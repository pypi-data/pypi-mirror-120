// Copyright (c) 2018 Microsoft Corporation
// Licensed under the MIT license.
// Author: Paul Koch <code@koch.ninja>

#include "precompiled_header_cpp.hpp"

#include <stdlib.h> // free
#include <stddef.h> // size_t, ptrdiff_t
#include <string.h> // memcpy

#include "ebm_native.h"
#include "logging.h"
#include "zones.h"

#include "ebm_internal.hpp"

#include "Feature.hpp"
#include "FeatureGroup.hpp"
#include "DataSetBoosting.hpp"

namespace DEFINED_ZONE_NAME {
#ifndef DEFINED_ZONE_NAME
#error DEFINED_ZONE_NAME must be defined
#endif // DEFINED_ZONE_NAME

INLINE_RELEASE_UNTEMPLATED static FloatEbmType * ConstructGradientsAndHessians(const bool bAllocateHessians, const size_t cSamples, const size_t cVectorLength) {
   LOG_0(TraceLevelInfo, "Entered ConstructGradientsAndHessians");

   EBM_ASSERT(1 <= cSamples);
   EBM_ASSERT(1 <= cVectorLength);

   const size_t cStorageItems = bAllocateHessians ? 2 : 1;
   if(IsMultiplyError(cVectorLength, cStorageItems, cSamples)) {
      LOG_0(TraceLevelWarning, "WARNING ConstructGradientsAndHessians IsMultiplyError(cVectorLength, cStorageItems, cSamples)");
      return nullptr;
   }
   const size_t cElements = cVectorLength * cStorageItems * cSamples;

   FloatEbmType * aGradientsAndHessians = EbmMalloc<FloatEbmType>(cElements);

   LOG_0(TraceLevelInfo, "Exited ConstructGradientsAndHessians");
   return aGradientsAndHessians;
}

INLINE_RELEASE_UNTEMPLATED static FloatEbmType * ConstructPredictorScores(
   const size_t cSamples, 
   const size_t cVectorLength, 
   const FloatEbmType * const aPredictorScoresFrom
) {
   LOG_0(TraceLevelInfo, "Entered DataSetBoosting::ConstructPredictorScores");

   EBM_ASSERT(0 < cSamples);
   EBM_ASSERT(0 < cVectorLength);
   EBM_ASSERT(nullptr != aPredictorScoresFrom);

   if(IsMultiplyError(cVectorLength, cSamples)) {
      LOG_0(TraceLevelWarning, "WARNING DataSetBoosting::ConstructPredictorScores IsMultiplyError(cVectorLength, cSamples)");
      return nullptr;
   }

   const size_t cElements = cVectorLength * cSamples;
   FloatEbmType * const aPredictorScoresTo = EbmMalloc<FloatEbmType>(cElements);
   if(nullptr == aPredictorScoresTo) {
      LOG_0(TraceLevelWarning, "WARNING DataSetBoosting::ConstructPredictorScores nullptr == aPredictorScoresTo");
      return nullptr;
   }

   const size_t cBytes = sizeof(FloatEbmType) * cElements;
   // if there are any NaN or +- infinity values we should just propagate them and exit during boosting
   memcpy(aPredictorScoresTo, aPredictorScoresFrom, cBytes);

#ifdef ZERO_FIRST_MULTICLASS_LOGIT

   if(2 <= cVectorLength) {
      FloatEbmType * pScore = aPredictorScoresTo;
      const FloatEbmType * const pScoreExteriorEnd = pScore + cVectorLength * cSamples;
      do {
         FloatEbmType scoreShift = pScore[0];
         const FloatEbmType * const pScoreInteriorEnd = pScore + cVectorLength;
         do {
            *pScore -= scoreShift;
            ++pScore;
         } while(pScoreInteriorEnd != pScore);
      } while(pScoreExteriorEnd != pScore);
   }

#endif // ZERO_FIRST_MULTICLASS_LOGIT

   LOG_0(TraceLevelInfo, "Exited DataSetBoosting::ConstructPredictorScores");
   return aPredictorScoresTo;
}

INLINE_RELEASE_UNTEMPLATED static StorageDataType * ConstructTargetData(
   const size_t cSamples, 
   const IntEbmType * const aTargets, 
   const ptrdiff_t runtimeLearningTypeOrCountTargetClasses
) {
   LOG_0(TraceLevelInfo, "Entered DataSetBoosting::ConstructTargetData");

   EBM_ASSERT(0 < cSamples);
   EBM_ASSERT(nullptr != aTargets);
   EBM_ASSERT(1 <= runtimeLearningTypeOrCountTargetClasses); // this should be classification
   const size_t countTargetClasses = static_cast<size_t>(runtimeLearningTypeOrCountTargetClasses);

   StorageDataType * const aTargetData = EbmMalloc<StorageDataType>(cSamples);
   if(nullptr == aTargetData) {
      LOG_0(TraceLevelWarning, "WARNING nullptr == aTargetData");
      return nullptr;
   }

   const IntEbmType * pTargetFrom = aTargets;
   const IntEbmType * const pTargetFromEnd = aTargets + cSamples;
   StorageDataType * pTargetTo = aTargetData;
   do {
      const IntEbmType data = *pTargetFrom;
      if(data < 0) {
         LOG_0(TraceLevelError, "ERROR DataSetBoosting::ConstructTargetData target value cannot be negative");
         free(aTargetData);
         return nullptr;
      }
      if(IsConvertError<StorageDataType>(data)) {
         // this shouldn't be possible since we previously checked that we could convert our target,
         // so if this is failing then we'll be larger than the maximum number of classes
         LOG_0(TraceLevelError, "ERROR DataSetBoosting::ConstructTargetData data target too big to reference memory");
         free(aTargetData);
         return nullptr;
      }
      if(IsConvertError<size_t>(data)) {
         // this shouldn't be possible since we previously checked that we could convert our target,
         // so if this is failing then we'll be larger than the maximum number of classes
         LOG_0(TraceLevelError, "ERROR DataSetBoosting::ConstructTargetData data target too big to reference memory");
         free(aTargetData);
         return nullptr;
      }
      const StorageDataType iData = static_cast<StorageDataType>(data);
      if(countTargetClasses <= static_cast<size_t>(iData)) {
         LOG_0(TraceLevelError, "ERROR DataSetBoosting::ConstructTargetData target value larger than number of classes");
         free(aTargetData);
         return nullptr;
      }
      *pTargetTo = iData;
      ++pTargetTo;
      ++pTargetFrom;
   } while(pTargetFromEnd != pTargetFrom);

   LOG_0(TraceLevelInfo, "Exited DataSetBoosting::ConstructTargetData");
   return aTargetData;
}

struct InputDataPointerAndCountBins {

   InputDataPointerAndCountBins() = default; // preserve our POD status
   ~InputDataPointerAndCountBins() = default; // preserve our POD status
   void * operator new(std::size_t) = delete; // we only use malloc/free in this library
   void operator delete (void *) = delete; // we only use malloc/free in this library

   const IntEbmType * m_pInputData;
   size_t m_cBins;
};
static_assert(std::is_standard_layout<InputDataPointerAndCountBins>::value,
   "We use the struct hack in several places, so disallow non-standard_layout types in general");
static_assert(std::is_trivial<InputDataPointerAndCountBins>::value,
   "We use memcpy in several places, so disallow non-trivial types in general");
static_assert(std::is_pod<InputDataPointerAndCountBins>::value,
   "We use a lot of C constructs, so disallow non-POD types in general");

INLINE_RELEASE_UNTEMPLATED static StorageDataType * * ConstructInputData(
   const size_t cFeatureGroups, 
   const FeatureGroup * const * const apFeatureGroup, 
   const size_t cSamples, 
   const IntEbmType * const aInputDataFrom
) {
   LOG_0(TraceLevelInfo, "Entered DataSetBoosting::ConstructInputData");

   EBM_ASSERT(0 < cFeatureGroups);
   EBM_ASSERT(nullptr != apFeatureGroup);
   EBM_ASSERT(0 < cSamples);
   // aInputDataFrom can be nullptr EVEN if 0 < cFeatureGroups && 0 < cSamples IF the featureGroups are all empty, 
   // which makes none of them refer to features, so the aInputDataFrom pointer isn't necessary

   StorageDataType ** const aaInputDataTo = EbmMalloc<StorageDataType *>(cFeatureGroups);
   if(nullptr == aaInputDataTo) {
      LOG_0(TraceLevelWarning, "WARNING DataSetBoosting::ConstructInputData nullptr == aaInputDataTo");
      return nullptr;
   }

   StorageDataType ** paInputDataTo = aaInputDataTo;
   const FeatureGroup * const * ppFeatureGroup = apFeatureGroup;
   const FeatureGroup * const * const ppFeatureGroupEnd = apFeatureGroup + cFeatureGroups;
   do {
      const FeatureGroup * const pFeatureGroup = *ppFeatureGroup;
      EBM_ASSERT(nullptr != pFeatureGroup);
      if(0 == pFeatureGroup->GetCountSignificantDimensions()) {
         *paInputDataTo = nullptr; // free will skip over these later
         ++paInputDataTo;
      } else {
         EBM_ASSERT(1 <= pFeatureGroup->GetBitPack());
         const size_t cItemsPerBitPack = static_cast<size_t>(pFeatureGroup->GetBitPack());
         // for a 32/64 bit storage item, we can't have more than 32/64 bit packed items stored
         EBM_ASSERT(cItemsPerBitPack <= CountBitsRequiredPositiveMax<StorageDataType>());
         const size_t cBitsPerItemMax = GetCountBits(cItemsPerBitPack);
         // if we have 1 item, it can't be larger than the number of bits of storage
         EBM_ASSERT(cBitsPerItemMax <= CountBitsRequiredPositiveMax<StorageDataType>());

         EBM_ASSERT(0 < cSamples);
         const size_t cDataUnits = (cSamples - 1) / cItemsPerBitPack + 1; // this can't overflow or underflow

         StorageDataType * pInputDataTo = EbmMalloc<StorageDataType>(cDataUnits);
         if(nullptr == pInputDataTo) {
            LOG_0(TraceLevelWarning, "WARNING DataSetBoosting::ConstructInputData nullptr == pInputDataTo");
            goto free_all;
         }
         *paInputDataTo = pInputDataTo;
         ++paInputDataTo;

         const size_t cBytesData = sizeof(StorageDataType) * cDataUnits;
         // stop on the last item in our array AND then do one special last loop with less or equal iterations to the normal loop
         const StorageDataType * const pInputDataToLast = 
            reinterpret_cast<const StorageDataType *>(reinterpret_cast<const char *>(pInputDataTo) + cBytesData) - 1;
         EBM_ASSERT(pInputDataTo <= pInputDataToLast); // we have 1 item or more, and therefore the last one can't be before the first item

         EBM_ASSERT(nullptr != aInputDataFrom);

         const FeatureGroupEntry * pFeatureGroupEntry = pFeatureGroup->GetFeatureGroupEntries();
         EBM_ASSERT(1 <= pFeatureGroup->GetCountDimensions());
         const FeatureGroupEntry * const pFeatureGroupEntryEnd = pFeatureGroupEntry + pFeatureGroup->GetCountDimensions();

         InputDataPointerAndCountBins dimensionInfo[k_cDimensionsMax];
         InputDataPointerAndCountBins * pDimensionInfoInit = &dimensionInfo[0];
         do {
            const Feature * const pFeature = pFeatureGroupEntry->m_pFeature;
            const size_t cBins = pFeature->GetCountBins();
            EBM_ASSERT(size_t { 1 } <= cBins); // we don't construct datasets on empty training sets
            if(size_t { 1 } < cBins) {
               pDimensionInfoInit->m_pInputData = &aInputDataFrom[pFeature->GetIndexFeatureData() * cSamples];
               pDimensionInfoInit->m_cBins = cBins;
               ++pDimensionInfoInit;
            }
            ++pFeatureGroupEntry;
         } while(pFeatureGroupEntryEnd != pFeatureGroupEntry);
         EBM_ASSERT(pDimensionInfoInit == &dimensionInfo[pFeatureGroup->GetCountSignificantDimensions()]);

         // THIS IS NOT A CONSTANT FOR A REASON.. WE CHANGE IT ON OUR LAST ITERATION
         // if we ever template this function on cItemsPerBitPack, then we'd want
         // to make this a constant so that the compiler could reason about it an eliminate loops
         // as it is, it isn't a constant, so the compiler would not be able to figure out that most
         // of the time it is a constant
         size_t shiftEnd = cBitsPerItemMax * cItemsPerBitPack;
         while(pInputDataTo < pInputDataToLast) /* do the last iteration AFTER we re-enter this loop through the goto label! */ {
         one_last_loop:;
            EBM_ASSERT(shiftEnd <= CountBitsRequiredPositiveMax<StorageDataType>());

            size_t bits = 0;
            size_t shift = 0;
            do {
               size_t tensorMultiple = 1;
               size_t tensorIndex = 0;
               InputDataPointerAndCountBins * pDimensionInfo = &dimensionInfo[0];
               do {
                  const IntEbmType * pInputData = pDimensionInfo->m_pInputData;
                  const IntEbmType inputData = *pInputData;
                  pDimensionInfo->m_pInputData = pInputData + 1;
                  if(inputData < 0) {
                     LOG_0(TraceLevelError, "ERROR DataSetBoosting::ConstructInputData inputData value cannot be negative");
                     goto free_all;
                  }
                  if(IsConvertError<size_t>(inputData)) {
                     LOG_0(TraceLevelError, "ERROR DataSetBoosting::ConstructInputData inputData value too big to reference memory");
                     goto free_all;
                  }
                  const size_t iData = static_cast<size_t>(inputData);

                  if(pDimensionInfo->m_cBins <= iData) {
                     LOG_0(TraceLevelError, "ERROR DataSetBoosting::ConstructInputData iData value must be less than the number of bins");
                     goto free_all;
                  }
                  // we check for overflows during FeatureGroup construction, but let's check here again
                  EBM_ASSERT(!IsMultiplyError(tensorMultiple, pDimensionInfo->m_cBins));

                  // this can't overflow if the multiplication below doesn't overflow, and we checked for that above
                  tensorIndex += tensorMultiple * iData;
                  tensorMultiple *= pDimensionInfo->m_cBins;

                  ++pDimensionInfo;
               } while(pDimensionInfoInit != pDimensionInfo);
               // put our first item in the least significant bits.  We do this so that later when
               // unpacking the indexes, we can just AND our mask with the bitfield to get the index and in subsequent loops
               // we can just shift down.  This eliminates one extra shift that we'd otherwise need to make if the first
               // item was in the MSB
               EBM_ASSERT(shift < CountBitsRequiredPositiveMax<StorageDataType>());
               bits |= tensorIndex << shift;
               shift += cBitsPerItemMax;
            } while(shiftEnd != shift);
            EBM_ASSERT(!IsConvertError<StorageDataType>(bits));
            *pInputDataTo = static_cast<StorageDataType>(bits);
            ++pInputDataTo;
         }

         if(pInputDataTo == pInputDataToLast) {
            // if this is the first time we've exited the loop, then re-enter it to do our last loop, but reduce the number of times we do the inner loop
            shiftEnd = cBitsPerItemMax * ((cSamples - 1) % cItemsPerBitPack + 1);
            goto one_last_loop;
         }
      }
      ++ppFeatureGroup;
   } while(ppFeatureGroupEnd != ppFeatureGroup);

   LOG_0(TraceLevelInfo, "Exited DataSetBoosting::ConstructInputData");
   return aaInputDataTo;

free_all:
   while(aaInputDataTo != paInputDataTo) {
      --paInputDataTo;
      free(*paInputDataTo);
   }
   free(aaInputDataTo);
   return nullptr;
}

ErrorEbmType DataSetBoosting::Initialize(
   const bool bAllocateGradients, 
   const bool bAllocateHessians,
   const bool bAllocatePredictorScores,
   const bool bAllocateTargetData, 
   const size_t cFeatureGroups, 
   const FeatureGroup * const * const apFeatureGroup, 
   const size_t cSamples, 
   const IntEbmType * const aInputDataFrom, 
   const void * const aTargets, 
   const FloatEbmType * const aPredictorScoresFrom, 
   const ptrdiff_t runtimeLearningTypeOrCountTargetClasses
) {
   EBM_ASSERT(nullptr == m_aGradientsAndHessians);
   EBM_ASSERT(nullptr == m_aPredictorScores);
   EBM_ASSERT(nullptr == m_aTargetData);
   EBM_ASSERT(nullptr == m_aaInputData);

   LOG_0(TraceLevelInfo, "Entered DataSetBoosting::Initialize");
   const size_t cVectorLength = GetVectorLength(runtimeLearningTypeOrCountTargetClasses);

   if(0 != cSamples) {
      if(bAllocateGradients) {
         FloatEbmType * aGradientsAndHessians = ConstructGradientsAndHessians(bAllocateHessians, cSamples, cVectorLength);
         if(nullptr == aGradientsAndHessians) {
            LOG_0(TraceLevelWarning, "WARNING Exited DataSetBoosting::Initialize nullptr == aGradientsAndHessians");
            return Error_OutOfMemory;
         }
         m_aGradientsAndHessians = aGradientsAndHessians;
      } else {
         EBM_ASSERT(!bAllocateHessians);
      }
      if(bAllocatePredictorScores) {
         FloatEbmType * aPredictorScores = ConstructPredictorScores(cSamples, cVectorLength, aPredictorScoresFrom);
         if(nullptr == aPredictorScores) {
            LOG_0(TraceLevelWarning, "WARNING Exited DataSetBoosting::Initialize nullptr == aPredictorScores");
            return Error_OutOfMemory;
         }
         m_aPredictorScores = aPredictorScores;
      }
      if(bAllocateTargetData) {
         StorageDataType * aTargetData = ConstructTargetData(cSamples, static_cast<const IntEbmType *>(aTargets), runtimeLearningTypeOrCountTargetClasses);
         if(nullptr == aTargetData) {
            LOG_0(TraceLevelWarning, "WARNING Exited DataSetBoosting::Initialize nullptr == aTargetData");
            return Error_OutOfMemory;
         }
         m_aTargetData = aTargetData;
      }
      if(0 != cFeatureGroups) {
         StorageDataType ** aaInputData = ConstructInputData(cFeatureGroups, apFeatureGroup, cSamples, aInputDataFrom);
         if(nullptr == aaInputData) {
            LOG_0(TraceLevelWarning, "WARNING Exited DataSetBoosting::Initialize nullptr == aaInputData");
            return Error_OutOfMemory;
         }
         m_aaInputData = aaInputData;
      }
      m_cSamples = cSamples;
      m_cFeatureGroups = cFeatureGroups;
   }

   LOG_0(TraceLevelInfo, "Exited DataSetBoosting::Initialize");

   return Error_None;
}

WARNING_PUSH
WARNING_DISABLE_USING_UNINITIALIZED_MEMORY
void DataSetBoosting::Destruct() {
   LOG_0(TraceLevelInfo, "Entered DataSetBoosting::Destruct");

   free(m_aGradientsAndHessians);
   free(m_aPredictorScores);
   free(m_aTargetData);

   if(nullptr != m_aaInputData) {
      EBM_ASSERT(0 < m_cFeatureGroups);
      StorageDataType * * paInputData = m_aaInputData;
      const StorageDataType * const * const paInputDataEnd = m_aaInputData + m_cFeatureGroups;
      do {
         free(*paInputData);
         ++paInputData;
      } while(paInputDataEnd != paInputData);
      free(m_aaInputData);
   }

   LOG_0(TraceLevelInfo, "Exited DataSetBoosting::Destruct");
}
WARNING_POP

} // DEFINED_ZONE_NAME
