// Copyright (c) 2018 Microsoft Corporation
// Licensed under the MIT license.
// Author: Paul Koch <ebm@koch.ninja>

#include "precompiled_header_cpp.hpp"

#include <stddef.h> // size_t, ptrdiff_t

#include "ebm_native.h"
#include "logging.h"
#include "zones.h"

#include "ebm_internal.hpp"

#include "approximate_math.hpp"
#include "ebm_stats.hpp"
// FeatureGroup.h depends on FeatureInternal.h
#include "FeatureGroup.hpp"
// dataset depends on features
#include "DataSetBoosting.hpp"

#include "BoosterCore.hpp"
#include "BoosterShell.hpp"

namespace DEFINED_ZONE_NAME {
#ifndef DEFINED_ZONE_NAME
#error DEFINED_ZONE_NAME must be defined
#endif // DEFINED_ZONE_NAME

// C++ does not allow partial function specialization, so we need to use these cumbersome static class functions to do partial function specialization

template<ptrdiff_t compilerLearningTypeOrCountTargetClasses>
class ApplyModelUpdateTrainingZeroFeatures final {
public:

   ApplyModelUpdateTrainingZeroFeatures() = delete; // this is a static class.  Do not construct

   static void Func(BoosterShell * const pBoosterShell) {
      static_assert(IsClassification(compilerLearningTypeOrCountTargetClasses), "must be classification");
      static_assert(!IsBinaryClassification(compilerLearningTypeOrCountTargetClasses), "must be multiclass");

      BoosterCore * const pBoosterCore = pBoosterShell->GetBoosterCore();
      const ptrdiff_t runtimeLearningTypeOrCountTargetClasses = pBoosterCore->GetRuntimeLearningTypeOrCountTargetClasses();
      DataSetBoosting * const pTrainingSet = pBoosterCore->GetTrainingSet();
      FloatEbmType * const aTempFloatVector = pBoosterShell->GetTempFloatVector();

      FloatEbmType aLocalExpVector[
         k_dynamicClassification == compilerLearningTypeOrCountTargetClasses ? 1 : GetVectorLength(compilerLearningTypeOrCountTargetClasses)
      ];
      FloatEbmType * const aExpVector = k_dynamicClassification == compilerLearningTypeOrCountTargetClasses ? aTempFloatVector : aLocalExpVector;

      const ptrdiff_t learningTypeOrCountTargetClasses = GET_LEARNING_TYPE_OR_COUNT_TARGET_CLASSES(
         compilerLearningTypeOrCountTargetClasses,
         runtimeLearningTypeOrCountTargetClasses
      );
      const size_t cVectorLength = GetVectorLength(learningTypeOrCountTargetClasses);
      const size_t cSamples = pTrainingSet->GetCountSamples();
      EBM_ASSERT(1 <= cSamples);

      const FloatEbmType * const aModelFeatureGroupUpdateTensor = pBoosterShell->GetAccumulatedModelUpdate()->GetValuePointer();
      EBM_ASSERT(nullptr != aModelFeatureGroupUpdateTensor);

      FloatEbmType * pGradientAndHessian = pTrainingSet->GetGradientsAndHessiansPointer();
      const StorageDataType * pTargetData = pTrainingSet->GetTargetDataPointer();
      FloatEbmType * pPredictorScores = pTrainingSet->GetPredictorScores();
      const FloatEbmType * const pPredictorScoresEnd = pPredictorScores + cSamples * cVectorLength;
      do {
         size_t targetData = static_cast<size_t>(*pTargetData);
         ++pTargetData;

         const FloatEbmType * pValues = aModelFeatureGroupUpdateTensor;
         FloatEbmType * pExpVector = aExpVector;
         FloatEbmType sumExp = FloatEbmType { 0 };
         size_t iVector = 0;
         do {
            // TODO : because there is only one bin for a zero feature feature group, we could move these values to the stack where the
            // compiler could reason about their visibility and optimize small arrays into registers
            const FloatEbmType smallChangeToPredictorScores = *pValues;
            ++pValues;
            // this will apply a small fix to our existing TrainingPredictorScores, either positive or negative, whichever is needed
            const FloatEbmType predictorScore = *pPredictorScores + smallChangeToPredictorScores;

#ifdef ZERO_FIRST_MULTICLASS_LOGIT
            if(IsMulticlass(compilerLearningTypeOrCountTargetClasses)) {
               if(size_t { 0 } == iVector) {
                  EBM_ASSERT(0 == smallChangeToPredictorScores);
                  EBM_ASSERT(0 == predictorScore);
               }
            }
#endif // ZERO_FIRST_MULTICLASS_LOGIT

            *pPredictorScores = predictorScore;
            ++pPredictorScores;
            const FloatEbmType oneExp = ExpForMulticlass<false>(predictorScore);
            *pExpVector = oneExp;
            ++pExpVector;
            sumExp += oneExp;
            ++iVector;
         } while(iVector < cVectorLength);
         pExpVector -= cVectorLength;
         iVector = 0;
         do {
            FloatEbmType gradient;
            FloatEbmType hessian;
            EbmStats::InverseLinkFunctionThenCalculateGradientAndHessianMulticlass(
               sumExp,
               *pExpVector,
               targetData,
               iVector,
               gradient,
               hessian
            );
            ++pExpVector;
            *pGradientAndHessian = gradient;
            *(pGradientAndHessian + 1) = hessian;
            pGradientAndHessian += 2;
            ++iVector;
         } while(iVector < cVectorLength);
      } while(pPredictorScoresEnd != pPredictorScores);
   }
};

#ifndef EXPAND_BINARY_LOGITS
template<>
class ApplyModelUpdateTrainingZeroFeatures<2> final {
public:

   ApplyModelUpdateTrainingZeroFeatures() = delete; // this is a static class.  Do not construct

   static void Func(BoosterShell * const pBoosterShell) {
      BoosterCore * const pBoosterCore = pBoosterShell->GetBoosterCore();
      DataSetBoosting * const pTrainingSet = pBoosterCore->GetTrainingSet();
      const size_t cSamples = pTrainingSet->GetCountSamples();
      EBM_ASSERT(1 <= cSamples);

      const FloatEbmType * const aModelFeatureGroupUpdateTensor = pBoosterShell->GetAccumulatedModelUpdate()->GetValuePointer();
      EBM_ASSERT(nullptr != aModelFeatureGroupUpdateTensor);

      FloatEbmType * pGradientAndHessian = pTrainingSet->GetGradientsAndHessiansPointer();
      const StorageDataType * pTargetData = pTrainingSet->GetTargetDataPointer();
      FloatEbmType * pPredictorScores = pTrainingSet->GetPredictorScores();
      const FloatEbmType * const pPredictorScoresEnd = pPredictorScores + cSamples;
      const FloatEbmType smallChangeToPredictorScores = aModelFeatureGroupUpdateTensor[0];
      do {
         size_t targetData = static_cast<size_t>(*pTargetData);
         ++pTargetData;
         // this will apply a small fix to our existing TrainingPredictorScores, either positive or negative, whichever is needed
         const FloatEbmType predictorScore = *pPredictorScores + smallChangeToPredictorScores;
         *pPredictorScores = predictorScore;
         ++pPredictorScores;
         const FloatEbmType gradient = EbmStats::InverseLinkFunctionThenCalculateGradientBinaryClassification(predictorScore, targetData);
         *pGradientAndHessian = gradient;
         *(pGradientAndHessian + 1) = EbmStats::CalculateHessianFromGradientBinaryClassification(gradient);
         pGradientAndHessian += 2;
      } while(pPredictorScoresEnd != pPredictorScores);
   }
};
#endif // EXPAND_BINARY_LOGITS

template<>
class ApplyModelUpdateTrainingZeroFeatures<k_regression> final {
public:

   ApplyModelUpdateTrainingZeroFeatures() = delete; // this is a static class.  Do not construct

   static void Func(BoosterShell * const pBoosterShell) {
      BoosterCore * const pBoosterCore = pBoosterShell->GetBoosterCore();
      DataSetBoosting * const pTrainingSet = pBoosterCore->GetTrainingSet();
      const size_t cSamples = pTrainingSet->GetCountSamples();
      EBM_ASSERT(1 <= cSamples);

      const FloatEbmType * const aModelFeatureGroupUpdateTensor = pBoosterShell->GetAccumulatedModelUpdate()->GetValuePointer();
      EBM_ASSERT(nullptr != aModelFeatureGroupUpdateTensor);

      // no hessian for regression
      FloatEbmType * pGradient = pTrainingSet->GetGradientsAndHessiansPointer();
      const FloatEbmType * const pGradientsEnd = pGradient + cSamples;
      const FloatEbmType smallChangeToPrediction = aModelFeatureGroupUpdateTensor[0];
      do {
         // this will apply a small fix to our existing TrainingPredictorScores, either positive or negative, whichever is needed
         const FloatEbmType gradient = EbmStats::ComputeGradientRegressionMSEFromOriginalGradient(*pGradient, smallChangeToPrediction);
         *pGradient = gradient;
         ++pGradient;
      } while(pGradientsEnd != pGradient);
   }
};

template<ptrdiff_t compilerLearningTypeOrCountTargetClassesPossible>
class ApplyModelUpdateTrainingZeroFeaturesTarget final {
public:

   ApplyModelUpdateTrainingZeroFeaturesTarget() = delete; // this is a static class.  Do not construct

   INLINE_ALWAYS static void Func(BoosterShell * const pBoosterShell) {
      static_assert(IsClassification(compilerLearningTypeOrCountTargetClassesPossible), "compilerLearningTypeOrCountTargetClassesPossible needs to be a classification");
      static_assert(compilerLearningTypeOrCountTargetClassesPossible <= k_cCompilerOptimizedTargetClassesMax, "We can't have this many items in a data pack.");

      BoosterCore * const pBoosterCore = pBoosterShell->GetBoosterCore();
      const ptrdiff_t runtimeLearningTypeOrCountTargetClasses = pBoosterCore->GetRuntimeLearningTypeOrCountTargetClasses();
      EBM_ASSERT(IsClassification(runtimeLearningTypeOrCountTargetClasses));
      EBM_ASSERT(runtimeLearningTypeOrCountTargetClasses <= k_cCompilerOptimizedTargetClassesMax);

      if(compilerLearningTypeOrCountTargetClassesPossible == runtimeLearningTypeOrCountTargetClasses) {
         ApplyModelUpdateTrainingZeroFeatures<compilerLearningTypeOrCountTargetClassesPossible>::Func(
            pBoosterShell
         );
      } else {
         ApplyModelUpdateTrainingZeroFeaturesTarget<
            compilerLearningTypeOrCountTargetClassesPossible + 1
         >::Func(
            pBoosterShell
         );
      }
   }
};

template<>
class ApplyModelUpdateTrainingZeroFeaturesTarget<k_cCompilerOptimizedTargetClassesMax + 1> final {
public:

   ApplyModelUpdateTrainingZeroFeaturesTarget() = delete; // this is a static class.  Do not construct

   INLINE_ALWAYS static void Func(BoosterShell * const pBoosterShell) {
      static_assert(IsClassification(k_cCompilerOptimizedTargetClassesMax), "k_cCompilerOptimizedTargetClassesMax needs to be a classification");

      EBM_ASSERT(IsClassification(pBoosterShell->GetBoosterCore()->GetRuntimeLearningTypeOrCountTargetClasses()));
      EBM_ASSERT(k_cCompilerOptimizedTargetClassesMax < pBoosterShell->GetBoosterCore()->GetRuntimeLearningTypeOrCountTargetClasses());

      ApplyModelUpdateTrainingZeroFeatures<k_dynamicClassification>::Func(pBoosterShell);
   }
};

template<ptrdiff_t compilerLearningTypeOrCountTargetClasses, size_t compilerBitPack>
class ApplyModelUpdateTrainingInternal final {
public:

   ApplyModelUpdateTrainingInternal() = delete; // this is a static class.  Do not construct

   static void Func(
      BoosterShell * const pBoosterShell,
      const FeatureGroup * const pFeatureGroup
   ) {
      static_assert(IsClassification(compilerLearningTypeOrCountTargetClasses), "must be classification");
      static_assert(!IsBinaryClassification(compilerLearningTypeOrCountTargetClasses), "must be multiclass");

      BoosterCore * const pBoosterCore = pBoosterShell->GetBoosterCore();
      const ptrdiff_t runtimeLearningTypeOrCountTargetClasses = pBoosterCore->GetRuntimeLearningTypeOrCountTargetClasses();
      DataSetBoosting * const pTrainingSet = pBoosterCore->GetTrainingSet();
      FloatEbmType * const aTempFloatVector = pBoosterShell->GetTempFloatVector();

      FloatEbmType aLocalExpVector[
         k_dynamicClassification == compilerLearningTypeOrCountTargetClasses ? 1 : GetVectorLength(compilerLearningTypeOrCountTargetClasses)
      ];
      FloatEbmType * const aExpVector = k_dynamicClassification == compilerLearningTypeOrCountTargetClasses ? aTempFloatVector : aLocalExpVector;

      const ptrdiff_t learningTypeOrCountTargetClasses = GET_LEARNING_TYPE_OR_COUNT_TARGET_CLASSES(
         compilerLearningTypeOrCountTargetClasses,
         runtimeLearningTypeOrCountTargetClasses
      );
      const size_t cVectorLength = GetVectorLength(learningTypeOrCountTargetClasses);
      const size_t cSamples = pTrainingSet->GetCountSamples();
      EBM_ASSERT(1 <= cSamples);
      EBM_ASSERT(1 <= pFeatureGroup->GetCountSignificantDimensions());

      const size_t cItemsPerBitPack = GET_ITEMS_PER_BIT_PACK(compilerBitPack, pFeatureGroup->GetBitPack());
      EBM_ASSERT(1 <= cItemsPerBitPack);
      EBM_ASSERT(cItemsPerBitPack <= k_cBitsForStorageType);
      const size_t cBitsPerItemMax = GetCountBits(cItemsPerBitPack);
      EBM_ASSERT(1 <= cBitsPerItemMax);
      EBM_ASSERT(cBitsPerItemMax <= k_cBitsForStorageType);
      const size_t maskBits = std::numeric_limits<size_t>::max() >> (k_cBitsForStorageType - cBitsPerItemMax);

      const FloatEbmType * const aModelFeatureGroupUpdateTensor = pBoosterShell->GetAccumulatedModelUpdate()->GetValuePointer();
      EBM_ASSERT(nullptr != aModelFeatureGroupUpdateTensor);

      FloatEbmType * pGradientAndHessian = pTrainingSet->GetGradientsAndHessiansPointer();
      const StorageDataType * pInputData = pTrainingSet->GetInputDataPointer(pFeatureGroup);
      const StorageDataType * pTargetData = pTrainingSet->GetTargetDataPointer();
      FloatEbmType * pPredictorScores = pTrainingSet->GetPredictorScores();

      // this shouldn't overflow since we're accessing existing memory
      const FloatEbmType * const pPredictorScoresTrueEnd = pPredictorScores + cSamples * cVectorLength;
      const FloatEbmType * pPredictorScoresExit = pPredictorScoresTrueEnd;
      const FloatEbmType * pPredictorScoresInnerEnd = pPredictorScoresTrueEnd;
      if(cSamples <= cItemsPerBitPack) {
         goto one_last_loop;
      }
      pPredictorScoresExit = pPredictorScoresTrueEnd - ((cSamples - 1) % cItemsPerBitPack + 1) * cVectorLength;
      EBM_ASSERT(pPredictorScores < pPredictorScoresExit);
      EBM_ASSERT(pPredictorScoresExit < pPredictorScoresTrueEnd);

      do {
         pPredictorScoresInnerEnd = pPredictorScores + cItemsPerBitPack * cVectorLength;
         // jumping back into this loop and changing pPredictorScoresInnerEnd to a dynamic value that isn't compile time determinable causes this 
         // function to NOT be optimized for templated cItemsPerBitPack, but that's ok since avoiding one unpredictable branch here is negligible
      one_last_loop:;
         // we store the already multiplied dimensional value in *pInputData
         size_t iTensorBinCombined = static_cast<size_t>(*pInputData);
         ++pInputData;
         do {
            size_t targetData = static_cast<size_t>(*pTargetData);
            ++pTargetData;

            const size_t iTensorBin = maskBits & iTensorBinCombined;
            const FloatEbmType * pValues = &aModelFeatureGroupUpdateTensor[iTensorBin * cVectorLength];
            FloatEbmType * pExpVector = aExpVector;
            FloatEbmType sumExp = FloatEbmType { 0 };
            size_t iVector = 0;
            do {
               const FloatEbmType smallChangeToPredictorScores = *pValues;
               ++pValues;
               // this will apply a small fix to our existing TrainingPredictorScores, either positive or negative, whichever is needed
               const FloatEbmType predictorScore = *pPredictorScores + smallChangeToPredictorScores;

#ifdef ZERO_FIRST_MULTICLASS_LOGIT
               if(IsMulticlass(compilerLearningTypeOrCountTargetClasses)) {
                  if(size_t { 0 } == iVector) {
                     EBM_ASSERT(0 == smallChangeToPredictorScores);
                     EBM_ASSERT(0 == predictorScore);
                  }
               }
#endif // ZERO_FIRST_MULTICLASS_LOGIT

               *pPredictorScores = predictorScore;
               ++pPredictorScores;
               const FloatEbmType oneExp = ExpForMulticlass<false>(predictorScore);
               *pExpVector = oneExp;
               ++pExpVector;
               sumExp += oneExp;
               ++iVector;
            } while(iVector < cVectorLength);
            pExpVector -= cVectorLength;
            iVector = 0;
            do {
               FloatEbmType gradient;
               FloatEbmType hessian;
               EbmStats::InverseLinkFunctionThenCalculateGradientAndHessianMulticlass(
                  sumExp,
                  *pExpVector,
                  targetData,
                  iVector,
                  gradient,
                  hessian
               );
               ++pExpVector;
               *pGradientAndHessian = gradient;
               *(pGradientAndHessian + 1) = hessian;
               pGradientAndHessian += 2;
               ++iVector;
            } while(iVector < cVectorLength);

            iTensorBinCombined >>= cBitsPerItemMax;
         } while(pPredictorScoresInnerEnd != pPredictorScores);
      } while(pPredictorScoresExit != pPredictorScores);

      // first time through?
      if(pPredictorScoresTrueEnd != pPredictorScores) {
         pPredictorScoresInnerEnd = pPredictorScoresTrueEnd;
         pPredictorScoresExit = pPredictorScoresTrueEnd;
         goto one_last_loop;
      }
   }
};

#ifndef EXPAND_BINARY_LOGITS
template<size_t compilerBitPack>
class ApplyModelUpdateTrainingInternal<2, compilerBitPack> final {
public:

   ApplyModelUpdateTrainingInternal() = delete; // this is a static class.  Do not construct

   static void Func(
      BoosterShell * const pBoosterShell,
      const FeatureGroup * const pFeatureGroup
   ) {
      BoosterCore * const pBoosterCore = pBoosterShell->GetBoosterCore();
      const size_t runtimeBitPack = pFeatureGroup->GetBitPack();
      DataSetBoosting * const pTrainingSet = pBoosterCore->GetTrainingSet();

      const size_t cSamples = pTrainingSet->GetCountSamples();
      EBM_ASSERT(1 <= cSamples);
      EBM_ASSERT(1 <= pFeatureGroup->GetCountSignificantDimensions());

      const size_t cItemsPerBitPack = GET_ITEMS_PER_BIT_PACK(compilerBitPack, runtimeBitPack);
      EBM_ASSERT(1 <= cItemsPerBitPack);
      EBM_ASSERT(cItemsPerBitPack <= k_cBitsForStorageType);
      const size_t cBitsPerItemMax = GetCountBits(cItemsPerBitPack);
      EBM_ASSERT(1 <= cBitsPerItemMax);
      EBM_ASSERT(cBitsPerItemMax <= k_cBitsForStorageType);
      const size_t maskBits = std::numeric_limits<size_t>::max() >> (k_cBitsForStorageType - cBitsPerItemMax);

      const FloatEbmType * const aModelFeatureGroupUpdateTensor = pBoosterShell->GetAccumulatedModelUpdate()->GetValuePointer();
      EBM_ASSERT(nullptr != aModelFeatureGroupUpdateTensor);

      FloatEbmType * pGradientAndHessian = pTrainingSet->GetGradientsAndHessiansPointer();
      const StorageDataType * pInputData = pTrainingSet->GetInputDataPointer(pFeatureGroup);
      const StorageDataType * pTargetData = pTrainingSet->GetTargetDataPointer();
      FloatEbmType * pPredictorScores = pTrainingSet->GetPredictorScores();

      // this shouldn't overflow since we're accessing existing memory
      const FloatEbmType * const pPredictorScoresTrueEnd = pPredictorScores + cSamples;
      const FloatEbmType * pPredictorScoresExit = pPredictorScoresTrueEnd;
      const FloatEbmType * pPredictorScoresInnerEnd = pPredictorScoresTrueEnd;
      if(cSamples <= cItemsPerBitPack) {
         goto one_last_loop;
      }
      pPredictorScoresExit = pPredictorScoresTrueEnd - ((cSamples - 1) % cItemsPerBitPack + 1);
      EBM_ASSERT(pPredictorScores < pPredictorScoresExit);
      EBM_ASSERT(pPredictorScoresExit < pPredictorScoresTrueEnd);

      do {
         pPredictorScoresInnerEnd = pPredictorScores + cItemsPerBitPack;
         // jumping back into this loop and changing pPredictorScoresInnerEnd to a dynamic value that isn't compile time determinable causes this 
         // function to NOT be optimized for templated cItemsPerBitPack, but that's ok since avoiding one unpredictable branch here is negligible
      one_last_loop:;
         // we store the already multiplied dimensional value in *pInputData
         size_t iTensorBinCombined = static_cast<size_t>(*pInputData);
         ++pInputData;
         do {
            size_t targetData = static_cast<size_t>(*pTargetData);
            ++pTargetData;

            const size_t iTensorBin = maskBits & iTensorBinCombined;

            const FloatEbmType smallChangeToPredictorScores = aModelFeatureGroupUpdateTensor[iTensorBin];
            // this will apply a small fix to our existing TrainingPredictorScores, either positive or negative, whichever is needed
            const FloatEbmType predictorScore = *pPredictorScores + smallChangeToPredictorScores;
            *pPredictorScores = predictorScore;
            ++pPredictorScores;
            const FloatEbmType gradient = EbmStats::InverseLinkFunctionThenCalculateGradientBinaryClassification(predictorScore, targetData);

            *pGradientAndHessian = gradient;
            *(pGradientAndHessian + 1) = EbmStats::CalculateHessianFromGradientBinaryClassification(gradient);
            pGradientAndHessian += 2;

            iTensorBinCombined >>= cBitsPerItemMax;
         } while(pPredictorScoresInnerEnd != pPredictorScores);
      } while(pPredictorScoresExit != pPredictorScores);

      // first time through?
      if(pPredictorScoresTrueEnd != pPredictorScores) {
         pPredictorScoresInnerEnd = pPredictorScoresTrueEnd;
         pPredictorScoresExit = pPredictorScoresTrueEnd;
         goto one_last_loop;
      }
   }
};
#endif // EXPAND_BINARY_LOGITS

template<size_t compilerBitPack>
class ApplyModelUpdateTrainingInternal<k_regression, compilerBitPack> final {
public:

   ApplyModelUpdateTrainingInternal() = delete; // this is a static class.  Do not construct

   static void Func(
      BoosterShell * const pBoosterShell,
      const FeatureGroup * const pFeatureGroup
   ) {
      BoosterCore * const pBoosterCore = pBoosterShell->GetBoosterCore();
      const size_t runtimeBitPack = pFeatureGroup->GetBitPack();
      DataSetBoosting * const pTrainingSet = pBoosterCore->GetTrainingSet();

      const size_t cSamples = pTrainingSet->GetCountSamples();
      EBM_ASSERT(1 <= cSamples);
      EBM_ASSERT(1 <= pFeatureGroup->GetCountSignificantDimensions());

      const size_t cItemsPerBitPack = GET_ITEMS_PER_BIT_PACK(compilerBitPack, runtimeBitPack);
      EBM_ASSERT(1 <= cItemsPerBitPack);
      EBM_ASSERT(cItemsPerBitPack <= k_cBitsForStorageType);
      const size_t cBitsPerItemMax = GetCountBits(cItemsPerBitPack);
      EBM_ASSERT(1 <= cBitsPerItemMax);
      EBM_ASSERT(cBitsPerItemMax <= k_cBitsForStorageType);
      const size_t maskBits = std::numeric_limits<size_t>::max() >> (k_cBitsForStorageType - cBitsPerItemMax);

      const FloatEbmType * const aModelFeatureGroupUpdateTensor = pBoosterShell->GetAccumulatedModelUpdate()->GetValuePointer();
      EBM_ASSERT(nullptr != aModelFeatureGroupUpdateTensor);

      // No hessians for regression
      FloatEbmType * pGradient = pTrainingSet->GetGradientsAndHessiansPointer();
      const StorageDataType * pInputData = pTrainingSet->GetInputDataPointer(pFeatureGroup);

      // this shouldn't overflow since we're accessing existing memory
      const FloatEbmType * const pGradientTrueEnd = pGradient + cSamples;
      const FloatEbmType * pGradientExit = pGradientTrueEnd;
      const FloatEbmType * pGradientInnerEnd = pGradientTrueEnd;
      if(cSamples <= cItemsPerBitPack) {
         goto one_last_loop;
      }
      pGradientExit = pGradientTrueEnd - ((cSamples - 1) % cItemsPerBitPack + 1);
      EBM_ASSERT(pGradient < pGradientExit);
      EBM_ASSERT(pGradientExit < pGradientTrueEnd);

      do {
         pGradientInnerEnd = pGradient + cItemsPerBitPack;
         // jumping back into this loop and changing pPredictorScoresInnerEnd to a dynamic value that isn't compile time determinable causes this 
         // function to NOT be optimized for templated cItemsPerBitPack, but that's ok since avoiding one unpredictable branch here is negligible
      one_last_loop:;
         // we store the already multiplied dimensional value in *pInputData
         size_t iTensorBinCombined = static_cast<size_t>(*pInputData);
         ++pInputData;
         do {
            const size_t iTensorBin = maskBits & iTensorBinCombined;

            const FloatEbmType smallChangeToPrediction = aModelFeatureGroupUpdateTensor[iTensorBin];
            // this will apply a small fix to our existing TrainingPredictorScores, either positive or negative, whichever is needed
            const FloatEbmType gradient = EbmStats::ComputeGradientRegressionMSEFromOriginalGradient(*pGradient, smallChangeToPrediction);

            *pGradient = gradient;
            ++pGradient;

            iTensorBinCombined >>= cBitsPerItemMax;
         } while(pGradientInnerEnd != pGradient);
      } while(pGradientExit != pGradient);

      // first time through?
      if(pGradientTrueEnd != pGradient) {
         pGradientInnerEnd = pGradientTrueEnd;
         pGradientExit = pGradientTrueEnd;
         goto one_last_loop;
      }
   }
};

template<ptrdiff_t compilerLearningTypeOrCountTargetClassesPossible>
class ApplyModelUpdateTrainingNormalTarget final {
public:

   ApplyModelUpdateTrainingNormalTarget() = delete; // this is a static class.  Do not construct

   INLINE_ALWAYS static void Func(
      BoosterShell * const pBoosterShell,
      const FeatureGroup * const pFeatureGroup
   ) {
      static_assert(IsClassification(compilerLearningTypeOrCountTargetClassesPossible), "compilerLearningTypeOrCountTargetClassesPossible needs to be a classification");
      static_assert(compilerLearningTypeOrCountTargetClassesPossible <= k_cCompilerOptimizedTargetClassesMax, "We can't have this many items in a data pack.");

      BoosterCore * const pBoosterCore = pBoosterShell->GetBoosterCore();
      const ptrdiff_t runtimeLearningTypeOrCountTargetClasses = pBoosterCore->GetRuntimeLearningTypeOrCountTargetClasses();
      EBM_ASSERT(IsClassification(runtimeLearningTypeOrCountTargetClasses));
      EBM_ASSERT(runtimeLearningTypeOrCountTargetClasses <= k_cCompilerOptimizedTargetClassesMax);

      if(compilerLearningTypeOrCountTargetClassesPossible == runtimeLearningTypeOrCountTargetClasses) {
         ApplyModelUpdateTrainingInternal<compilerLearningTypeOrCountTargetClassesPossible, k_cItemsPerBitPackDynamic>::Func(
            pBoosterShell,
            pFeatureGroup
         );
      } else {
         ApplyModelUpdateTrainingNormalTarget<
            compilerLearningTypeOrCountTargetClassesPossible + 1
         >::Func(
            pBoosterShell,
            pFeatureGroup
         );
      }
   }
};

template<>
class ApplyModelUpdateTrainingNormalTarget<k_cCompilerOptimizedTargetClassesMax + 1> final {
public:

   ApplyModelUpdateTrainingNormalTarget() = delete; // this is a static class.  Do not construct

   INLINE_ALWAYS static void Func(
      BoosterShell * const pBoosterShell,
      const FeatureGroup * const pFeatureGroup
   ) {
      static_assert(IsClassification(k_cCompilerOptimizedTargetClassesMax), "k_cCompilerOptimizedTargetClassesMax needs to be a classification");

      EBM_ASSERT(IsClassification(pBoosterShell->GetBoosterCore()->GetRuntimeLearningTypeOrCountTargetClasses()));
      EBM_ASSERT(k_cCompilerOptimizedTargetClassesMax < pBoosterShell->GetBoosterCore()->GetRuntimeLearningTypeOrCountTargetClasses());

      ApplyModelUpdateTrainingInternal<k_dynamicClassification, k_cItemsPerBitPackDynamic>::Func(
         pBoosterShell,
         pFeatureGroup
      );
   }
};

template<ptrdiff_t compilerLearningTypeOrCountTargetClasses, size_t compilerBitPack>
class ApplyModelUpdateTrainingSIMDPacking final {
public:

   ApplyModelUpdateTrainingSIMDPacking() = delete; // this is a static class.  Do not construct

   INLINE_ALWAYS static void Func(
      BoosterShell * const pBoosterShell,
      const FeatureGroup * const pFeatureGroup
   ) {
      const size_t runtimeBitPack = pFeatureGroup->GetBitPack();

      EBM_ASSERT(1 <= runtimeBitPack);
      EBM_ASSERT(runtimeBitPack <= k_cBitsForStorageType);
      static_assert(compilerBitPack <= k_cBitsForStorageType, "We can't have this many items in a data pack.");
      if(compilerBitPack == runtimeBitPack) {
         ApplyModelUpdateTrainingInternal<compilerLearningTypeOrCountTargetClasses, compilerBitPack>::Func(
            pBoosterShell,
            pFeatureGroup
         );
      } else {
         ApplyModelUpdateTrainingSIMDPacking<
            compilerLearningTypeOrCountTargetClasses,
            GetNextCountItemsBitPacked(compilerBitPack)
         >::Func(
            pBoosterShell,
            pFeatureGroup
         );
      }
   }
};

template<ptrdiff_t compilerLearningTypeOrCountTargetClasses>
class ApplyModelUpdateTrainingSIMDPacking<compilerLearningTypeOrCountTargetClasses, k_cItemsPerBitPackDynamic> final {
public:

   ApplyModelUpdateTrainingSIMDPacking() = delete; // this is a static class.  Do not construct

   INLINE_ALWAYS static void Func(
      BoosterShell * const pBoosterShell,
      const FeatureGroup * const pFeatureGroup
   ) {
      EBM_ASSERT(1 <= pFeatureGroup->GetBitPack());
      EBM_ASSERT(pFeatureGroup->GetBitPack() <= static_cast<ptrdiff_t>(k_cBitsForStorageType));
      ApplyModelUpdateTrainingInternal<compilerLearningTypeOrCountTargetClasses, k_cItemsPerBitPackDynamic>::Func(
         pBoosterShell,
         pFeatureGroup
      );
   }
};

template<ptrdiff_t compilerLearningTypeOrCountTargetClassesPossible>
class ApplyModelUpdateTrainingSIMDTarget final {
public:

   ApplyModelUpdateTrainingSIMDTarget() = delete; // this is a static class.  Do not construct

   INLINE_ALWAYS static void Func(
      BoosterShell * const pBoosterShell,
      const FeatureGroup * const pFeatureGroup
   ) {
      static_assert(IsClassification(compilerLearningTypeOrCountTargetClassesPossible), "compilerLearningTypeOrCountTargetClassesPossible needs to be a classification");
      static_assert(compilerLearningTypeOrCountTargetClassesPossible <= k_cCompilerOptimizedTargetClassesMax, "We can't have this many items in a data pack.");

      BoosterCore * const pBoosterCore = pBoosterShell->GetBoosterCore();
      const ptrdiff_t runtimeLearningTypeOrCountTargetClasses = pBoosterCore->GetRuntimeLearningTypeOrCountTargetClasses();
      EBM_ASSERT(IsClassification(runtimeLearningTypeOrCountTargetClasses));
      EBM_ASSERT(runtimeLearningTypeOrCountTargetClasses <= k_cCompilerOptimizedTargetClassesMax);

      if(compilerLearningTypeOrCountTargetClassesPossible == runtimeLearningTypeOrCountTargetClasses) {
         ApplyModelUpdateTrainingSIMDPacking<
            compilerLearningTypeOrCountTargetClassesPossible,
            k_cItemsPerBitPackMax
         >::Func(
            pBoosterShell,
            pFeatureGroup
         );
      } else {
         ApplyModelUpdateTrainingSIMDTarget<
            compilerLearningTypeOrCountTargetClassesPossible + 1
         >::Func(
            pBoosterShell,
            pFeatureGroup
         );
      }
   }
};

template<>
class ApplyModelUpdateTrainingSIMDTarget<k_cCompilerOptimizedTargetClassesMax + 1> final {
public:

   ApplyModelUpdateTrainingSIMDTarget() = delete; // this is a static class.  Do not construct

   INLINE_ALWAYS static void Func(
      BoosterShell * const pBoosterShell,
      const FeatureGroup * const pFeatureGroup
   ) {
      static_assert(IsClassification(k_cCompilerOptimizedTargetClassesMax), "k_cCompilerOptimizedTargetClassesMax needs to be a classification");

      EBM_ASSERT(IsClassification(pBoosterShell->GetBoosterCore()->GetRuntimeLearningTypeOrCountTargetClasses()));
      EBM_ASSERT(k_cCompilerOptimizedTargetClassesMax < pBoosterShell->GetBoosterCore()->GetRuntimeLearningTypeOrCountTargetClasses());

      ApplyModelUpdateTrainingSIMDPacking<k_dynamicClassification, k_cItemsPerBitPackMax>::Func(
         pBoosterShell,
         pFeatureGroup
      );
   }
};

extern void ApplyModelUpdateTraining(
   BoosterShell * const pBoosterShell,
   const FeatureGroup * const pFeatureGroup
) {
   LOG_0(TraceLevelVerbose, "Entered ApplyModelUpdateTraining");

   BoosterCore * const pBoosterCore = pBoosterShell->GetBoosterCore();
   const ptrdiff_t runtimeLearningTypeOrCountTargetClasses = pBoosterCore->GetRuntimeLearningTypeOrCountTargetClasses();

   if(0 == pFeatureGroup->GetCountSignificantDimensions()) {
      if(IsClassification(runtimeLearningTypeOrCountTargetClasses)) {
         ApplyModelUpdateTrainingZeroFeaturesTarget<2>::Func(pBoosterShell);
      } else {
         EBM_ASSERT(IsRegression(runtimeLearningTypeOrCountTargetClasses));
         ApplyModelUpdateTrainingZeroFeatures<k_regression>::Func(pBoosterShell);
      }
   } else {
      if(k_bUseSIMD) {
         // TODO : enable SIMD(AVX-512) to work

         // 64 - do 8 at a time and unroll the loop 8 times.  These are bool features and are common.  Put the unrolled inner loop into a function
         // 32 - do 8 at a time and unroll the loop 4 times.  These are bool features and are common.  Put the unrolled inner loop into a function
         // 21 - do 8 at a time and unroll the loop 3 times (ignore the last 3 with a mask)
         // 16 - do 8 at a time and unroll the loop 2 times.  These are bool features and are common.  Put the unrolled inner loop into a function
         // 12 - do 8 of them, shift the low 4 upwards and then load the next 12 and take the top 4, repeat.
         // 10 - just drop this down to packing 8 together
         // 9 - just drop this down to packing 8 together
         // 8 - do all 8 at a time without an inner loop.  This is one of the most common values.  256 binned values
         // 7,6,5,4,3,2,1 - use a mask to exclude the non-used conditions and process them like the 8.  These are rare since they require more than 256 values

         if(IsClassification(runtimeLearningTypeOrCountTargetClasses)) {
            ApplyModelUpdateTrainingSIMDTarget<2>::Func(pBoosterShell, pFeatureGroup);
         } else {
            EBM_ASSERT(IsRegression(runtimeLearningTypeOrCountTargetClasses));
            ApplyModelUpdateTrainingSIMDPacking<k_regression, k_cItemsPerBitPackMax>::Func(
               pBoosterShell,
               pFeatureGroup
            );
         }
      } else {
         // there isn't much benefit in eliminating the loop that unpacks a data unit unless we're also unpacking that to SIMD code
         // Our default packing structure is to bin continuous values to 256 values, and we have 64 bit packing structures, so we usually
         // have more than 8 values per memory fetch.  Eliminating the inner loop for multiclass is valuable since we can have low numbers like 3 class,
         // 4 class, etc, but by the time we get to 8 loops with exp inside and a lot of other instructures we should worry that our code expansion
         // will exceed the L1 instruction cache size.  With SIMD we do 8 times the work in the same number of instructions so these are lesser issues

         if(IsClassification(runtimeLearningTypeOrCountTargetClasses)) {
            ApplyModelUpdateTrainingNormalTarget<2>::Func(pBoosterShell, pFeatureGroup);
         } else {
            EBM_ASSERT(IsRegression(runtimeLearningTypeOrCountTargetClasses));
            ApplyModelUpdateTrainingInternal<k_regression, k_cItemsPerBitPackDynamic>::Func(
               pBoosterShell,
               pFeatureGroup
            );
         }
      }
   }

   LOG_0(TraceLevelVerbose, "Exited ApplyModelUpdateTraining");
}

} // DEFINED_ZONE_NAME
