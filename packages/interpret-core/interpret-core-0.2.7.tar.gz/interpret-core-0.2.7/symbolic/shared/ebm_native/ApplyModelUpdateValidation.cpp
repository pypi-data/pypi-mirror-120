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
class ApplyModelUpdateValidationZeroFeatures final {
public:

   ApplyModelUpdateValidationZeroFeatures() = delete; // this is a static class.  Do not construct

   static FloatEbmType Func(BoosterShell * const pBoosterShell) {
      static_assert(IsClassification(compilerLearningTypeOrCountTargetClasses), "must be classification");
      static_assert(!IsBinaryClassification(compilerLearningTypeOrCountTargetClasses), "must be multiclass");

      BoosterCore * const pBoosterCore = pBoosterShell->GetBoosterCore();
      const FloatEbmType * const aModelFeatureGroupUpdateTensor = pBoosterShell->GetAccumulatedModelUpdate()->GetValuePointer();
      EBM_ASSERT(nullptr != aModelFeatureGroupUpdateTensor);

      const ptrdiff_t runtimeLearningTypeOrCountTargetClasses = pBoosterCore->GetRuntimeLearningTypeOrCountTargetClasses();
      DataSetBoosting * const pValidationSet = pBoosterCore->GetValidationSet();
      const FloatEbmType * pWeight = pBoosterCore->GetValidationWeights();
#ifndef NDEBUG
      FloatEbmType weightTotalDebug = 0;
#endif // NDEBUG

      const ptrdiff_t learningTypeOrCountTargetClasses = GET_LEARNING_TYPE_OR_COUNT_TARGET_CLASSES(
         compilerLearningTypeOrCountTargetClasses,
         runtimeLearningTypeOrCountTargetClasses
      );
      const size_t cVectorLength = GetVectorLength(learningTypeOrCountTargetClasses);
      const size_t cSamples = pValidationSet->GetCountSamples();
      EBM_ASSERT(0 < cSamples);

      FloatEbmType sumLogLoss = FloatEbmType { 0 };
      const StorageDataType * pTargetData = pValidationSet->GetTargetDataPointer();
      FloatEbmType * pPredictorScores = pValidationSet->GetPredictorScores();
      const FloatEbmType * const pPredictorScoresEnd = pPredictorScores + cSamples * cVectorLength;
      do {
         size_t targetData = static_cast<size_t>(*pTargetData);
         ++pTargetData;

         const FloatEbmType * pValues = aModelFeatureGroupUpdateTensor;
         FloatEbmType itemExp = FloatEbmType { 0 };
         FloatEbmType sumExp = FloatEbmType { 0 };
         size_t iVector = 0;
         do {
            // TODO : because there is only one bin for a zero feature feature group, we could move these values to the stack where the
            // compiler could reason about their visibility and optimize small arrays into registers
            const FloatEbmType smallChangeToPredictorScores = *pValues;
            ++pValues;
            // this will apply a small fix to our existing ValidationPredictorScores, either positive or negative, whichever is needed
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
            const FloatEbmType oneExp = ExpForLogLossMulticlass<false>(predictorScore);
            itemExp = iVector == targetData ? oneExp : itemExp;
            sumExp += oneExp;
            ++iVector;
         } while(iVector < cVectorLength);
         const FloatEbmType sampleLogLoss = EbmStats::ComputeSingleSampleLogLossMulticlass(
            sumExp,
            itemExp
         );

         EBM_ASSERT(std::isnan(sampleLogLoss) || -k_epsilonLogLoss <= sampleLogLoss);

         FloatEbmType weight = FloatEbmType { 1 };
         if(nullptr != pWeight) {
            // TODO: template this check away
            weight = *pWeight;
            ++pWeight;
#ifndef NDEBUG
            weightTotalDebug += weight;
#endif // NDEBUG
         }
         sumLogLoss += sampleLogLoss * weight;
      } while(pPredictorScoresEnd != pPredictorScores);
      const FloatEbmType totalWeight = pBoosterCore->GetValidationWeightTotal();

      EBM_ASSERT(FloatEbmType { 0 } < totalWeight);
      EBM_ASSERT(nullptr == pWeight || totalWeight * 0.999 <= weightTotalDebug &&
         weightTotalDebug <= 1.001 * totalWeight);
      EBM_ASSERT(nullptr != pWeight || static_cast<FloatEbmType>(cSamples) == totalWeight);

      return sumLogLoss / totalWeight;
   }
};

#ifndef EXPAND_BINARY_LOGITS
template<>
class ApplyModelUpdateValidationZeroFeatures<2> final {
public:

   ApplyModelUpdateValidationZeroFeatures() = delete; // this is a static class.  Do not construct

   static FloatEbmType Func(BoosterShell * const pBoosterShell) {
      BoosterCore * const pBoosterCore = pBoosterShell->GetBoosterCore();
      const FloatEbmType * const aModelFeatureGroupUpdateTensor = pBoosterShell->GetAccumulatedModelUpdate()->GetValuePointer();
      EBM_ASSERT(nullptr != aModelFeatureGroupUpdateTensor);

      DataSetBoosting * const pValidationSet = pBoosterCore->GetValidationSet();
      const size_t cSamples = pValidationSet->GetCountSamples();
      EBM_ASSERT(0 < cSamples);

      const FloatEbmType * pWeight = pBoosterCore->GetValidationWeights();
#ifndef NDEBUG
      FloatEbmType weightTotalDebug = 0;
#endif // NDEBUG

      FloatEbmType sumLogLoss = 0;
      const StorageDataType * pTargetData = pValidationSet->GetTargetDataPointer();
      FloatEbmType * pPredictorScores = pValidationSet->GetPredictorScores();
      const FloatEbmType * const pPredictorScoresEnd = pPredictorScores + cSamples;
      const FloatEbmType smallChangeToPredictorScores = aModelFeatureGroupUpdateTensor[0];
      do {
         size_t targetData = static_cast<size_t>(*pTargetData);
         ++pTargetData;
         // this will apply a small fix to our existing ValidationPredictorScores, either positive or negative, whichever is needed
         const FloatEbmType predictorScore = *pPredictorScores + smallChangeToPredictorScores;
         *pPredictorScores = predictorScore;
         ++pPredictorScores;
         const FloatEbmType sampleLogLoss = EbmStats::ComputeSingleSampleLogLossBinaryClassification(predictorScore, targetData);
         EBM_ASSERT(std::isnan(sampleLogLoss) || FloatEbmType { 0 } <= sampleLogLoss);

         FloatEbmType weight = FloatEbmType { 1 };
         if(nullptr != pWeight) {
            // TODO: template this check away
            weight = *pWeight;
            ++pWeight;
#ifndef NDEBUG
            weightTotalDebug += weight;
#endif // NDEBUG
         }
         sumLogLoss += sampleLogLoss * weight;
      } while(pPredictorScoresEnd != pPredictorScores);
      const FloatEbmType totalWeight = pBoosterCore->GetValidationWeightTotal();

      EBM_ASSERT(FloatEbmType { 0 } < totalWeight);
      EBM_ASSERT(nullptr == pWeight || totalWeight * 0.999 <= weightTotalDebug &&
         weightTotalDebug <= 1.001 * totalWeight);
      EBM_ASSERT(nullptr != pWeight || static_cast<FloatEbmType>(cSamples) == totalWeight);

      return sumLogLoss / totalWeight;
   }
};
#endif // EXPAND_BINARY_LOGITS

template<>
class ApplyModelUpdateValidationZeroFeatures<k_regression> final {
public:

   ApplyModelUpdateValidationZeroFeatures() = delete; // this is a static class.  Do not construct

   static FloatEbmType Func(BoosterShell * const pBoosterShell) {
      BoosterCore * const pBoosterCore = pBoosterShell->GetBoosterCore();
      const FloatEbmType * const aModelFeatureGroupUpdateTensor = pBoosterShell->GetAccumulatedModelUpdate()->GetValuePointer();
      EBM_ASSERT(nullptr != aModelFeatureGroupUpdateTensor);

      DataSetBoosting * const pValidationSet = pBoosterCore->GetValidationSet();
      const size_t cSamples = pValidationSet->GetCountSamples();
      EBM_ASSERT(0 < cSamples);

      const FloatEbmType * pWeight = pBoosterCore->GetValidationWeights();
#ifndef NDEBUG
      FloatEbmType weightTotalDebug = 0;
#endif // NDEBUG

      FloatEbmType sumSquareError = FloatEbmType { 0 };
      // no hessians for regression
      FloatEbmType * pGradient = pValidationSet->GetGradientsAndHessiansPointer();
      const FloatEbmType * const pGradientsEnd = pGradient + cSamples;
      const FloatEbmType smallChangeToPrediction = aModelFeatureGroupUpdateTensor[0];
      do {
         // this will apply a small fix to our existing ValidationPredictorScores, either positive or negative, whichever is needed
         const FloatEbmType gradient = EbmStats::ComputeGradientRegressionMSEFromOriginalGradient(*pGradient, smallChangeToPrediction);
         const FloatEbmType singleSampleSquaredError = EbmStats::ComputeSingleSampleSquaredErrorRegressionFromGradient(gradient);
         EBM_ASSERT(std::isnan(singleSampleSquaredError) || FloatEbmType { 0 } <= singleSampleSquaredError);

         FloatEbmType weight = FloatEbmType { 1 };
         if(nullptr != pWeight) {
            // TODO: template this check away
            weight = *pWeight;
            ++pWeight;
#ifndef NDEBUG
            weightTotalDebug += weight;
#endif // NDEBUG
         }
         sumSquareError += singleSampleSquaredError * weight;
         *pGradient = gradient;
         ++pGradient;
      } while(pGradientsEnd != pGradient);
      const FloatEbmType totalWeight = pBoosterCore->GetValidationWeightTotal();

      EBM_ASSERT(FloatEbmType { 0 } < totalWeight);
      EBM_ASSERT(nullptr == pWeight || totalWeight * 0.999 <= weightTotalDebug &&
         weightTotalDebug <= 1.001 * totalWeight);
      EBM_ASSERT(nullptr != pWeight || static_cast<FloatEbmType>(cSamples) == totalWeight);

      return sumSquareError / totalWeight;
   }
};

template<ptrdiff_t compilerLearningTypeOrCountTargetClassesPossible>
class ApplyModelUpdateValidationZeroFeaturesTarget final {
public:

   ApplyModelUpdateValidationZeroFeaturesTarget() = delete; // this is a static class.  Do not construct

   INLINE_ALWAYS static FloatEbmType Func(BoosterShell * const pBoosterShell) {
      static_assert(IsClassification(compilerLearningTypeOrCountTargetClassesPossible), "compilerLearningTypeOrCountTargetClassesPossible needs to be a classification");
      static_assert(compilerLearningTypeOrCountTargetClassesPossible <= k_cCompilerOptimizedTargetClassesMax, "We can't have this many items in a data pack.");

      BoosterCore * const pBoosterCore = pBoosterShell->GetBoosterCore();
      const ptrdiff_t runtimeLearningTypeOrCountTargetClasses = pBoosterCore->GetRuntimeLearningTypeOrCountTargetClasses();
      EBM_ASSERT(IsClassification(runtimeLearningTypeOrCountTargetClasses));
      EBM_ASSERT(runtimeLearningTypeOrCountTargetClasses <= k_cCompilerOptimizedTargetClassesMax);

      if(compilerLearningTypeOrCountTargetClassesPossible == runtimeLearningTypeOrCountTargetClasses) {
         return ApplyModelUpdateValidationZeroFeatures<compilerLearningTypeOrCountTargetClassesPossible>::Func(
            pBoosterShell
         );
      } else {
         return ApplyModelUpdateValidationZeroFeaturesTarget<
            compilerLearningTypeOrCountTargetClassesPossible + 1
         >::Func(
            pBoosterShell
         );
      }
   }
};

template<>
class ApplyModelUpdateValidationZeroFeaturesTarget<k_cCompilerOptimizedTargetClassesMax + 1> final {
public:

   ApplyModelUpdateValidationZeroFeaturesTarget() = delete; // this is a static class.  Do not construct

   INLINE_ALWAYS static FloatEbmType Func(BoosterShell * const pBoosterShell) {
      static_assert(IsClassification(k_cCompilerOptimizedTargetClassesMax), "k_cCompilerOptimizedTargetClassesMax needs to be a classification");

      EBM_ASSERT(IsClassification(pBoosterShell->GetBoosterCore()->GetRuntimeLearningTypeOrCountTargetClasses()));
      EBM_ASSERT(k_cCompilerOptimizedTargetClassesMax < pBoosterShell->GetBoosterCore()->GetRuntimeLearningTypeOrCountTargetClasses());

      return ApplyModelUpdateValidationZeroFeatures<k_dynamicClassification>::Func(pBoosterShell);
   }
};

template<ptrdiff_t compilerLearningTypeOrCountTargetClasses, size_t compilerBitPack>
class ApplyModelUpdateValidationInternal final {
public:

   ApplyModelUpdateValidationInternal() = delete; // this is a static class.  Do not construct

   static FloatEbmType Func(
      BoosterShell * const pBoosterShell,
      const FeatureGroup * const pFeatureGroup
   ) {
      static_assert(IsClassification(compilerLearningTypeOrCountTargetClasses), "must be classification");
      static_assert(!IsBinaryClassification(compilerLearningTypeOrCountTargetClasses), "must be multiclass");

      BoosterCore * const pBoosterCore = pBoosterShell->GetBoosterCore();
      const FloatEbmType * const aModelFeatureGroupUpdateTensor = pBoosterShell->GetAccumulatedModelUpdate()->GetValuePointer();
      EBM_ASSERT(nullptr != aModelFeatureGroupUpdateTensor);

      const ptrdiff_t runtimeLearningTypeOrCountTargetClasses = pBoosterCore->GetRuntimeLearningTypeOrCountTargetClasses();
      const size_t runtimeBitPack = pFeatureGroup->GetBitPack();
      DataSetBoosting * const pValidationSet = pBoosterCore->GetValidationSet();
      const FloatEbmType * pWeight = pBoosterCore->GetValidationWeights();
#ifndef NDEBUG
      FloatEbmType weightTotalDebug = 0;
#endif // NDEBUG

      const ptrdiff_t learningTypeOrCountTargetClasses = GET_LEARNING_TYPE_OR_COUNT_TARGET_CLASSES(
         compilerLearningTypeOrCountTargetClasses,
         runtimeLearningTypeOrCountTargetClasses
      );
      const size_t cVectorLength = GetVectorLength(learningTypeOrCountTargetClasses);
      const size_t cSamples = pValidationSet->GetCountSamples();
      EBM_ASSERT(1 <= cSamples);
      EBM_ASSERT(1 <= pFeatureGroup->GetCountSignificantDimensions());

      const size_t cItemsPerBitPack = GET_ITEMS_PER_BIT_PACK(compilerBitPack, runtimeBitPack);
      EBM_ASSERT(1 <= cItemsPerBitPack);
      EBM_ASSERT(cItemsPerBitPack <= k_cBitsForStorageType);
      const size_t cBitsPerItemMax = GetCountBits(cItemsPerBitPack);
      EBM_ASSERT(1 <= cBitsPerItemMax);
      EBM_ASSERT(cBitsPerItemMax <= k_cBitsForStorageType);
      const size_t maskBits = std::numeric_limits<size_t>::max() >> (k_cBitsForStorageType - cBitsPerItemMax);

      FloatEbmType sumLogLoss = FloatEbmType { 0 };
      const StorageDataType * pInputData = pValidationSet->GetInputDataPointer(pFeatureGroup);
      const StorageDataType * pTargetData = pValidationSet->GetTargetDataPointer();
      FloatEbmType * pPredictorScores = pValidationSet->GetPredictorScores();

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
            FloatEbmType itemExp = FloatEbmType { 0 };
            FloatEbmType sumExp = FloatEbmType { 0 };
            size_t iVector = 0;
            do {
               const FloatEbmType smallChangeToPredictorScores = *pValues;
               ++pValues;
               // this will apply a small fix to our existing ValidationPredictorScores, either positive or negative, whichever is needed
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
               const FloatEbmType oneExp = ExpForLogLossMulticlass<false>(predictorScore);
               itemExp = iVector == targetData ? oneExp : itemExp;
               sumExp += oneExp;
               ++iVector;
            } while(iVector < cVectorLength);
            const FloatEbmType sampleLogLoss = EbmStats::ComputeSingleSampleLogLossMulticlass(
               sumExp,
               itemExp
            );

            EBM_ASSERT(std::isnan(sampleLogLoss) || -k_epsilonLogLoss <= sampleLogLoss);

            FloatEbmType weight = FloatEbmType { 1 };
            if(nullptr != pWeight) {
               // TODO: template this check away
               weight = *pWeight;
               ++pWeight;
#ifndef NDEBUG
               weightTotalDebug += weight;
#endif // NDEBUG
            }
            sumLogLoss += sampleLogLoss * weight;
            iTensorBinCombined >>= cBitsPerItemMax;
         } while(pPredictorScoresInnerEnd != pPredictorScores);
      } while(pPredictorScoresExit != pPredictorScores);

      // first time through?
      if(pPredictorScoresTrueEnd != pPredictorScores) {
         pPredictorScoresInnerEnd = pPredictorScoresTrueEnd;
         pPredictorScoresExit = pPredictorScoresTrueEnd;
         goto one_last_loop;
      }
      const FloatEbmType totalWeight = pBoosterCore->GetValidationWeightTotal();

      EBM_ASSERT(FloatEbmType { 0 } < totalWeight);
      EBM_ASSERT(nullptr == pWeight || totalWeight * 0.999 <= weightTotalDebug &&
         weightTotalDebug <= 1.001 * totalWeight);
      EBM_ASSERT(nullptr != pWeight || static_cast<FloatEbmType>(cSamples) == totalWeight);

      return sumLogLoss / totalWeight;
   }
};

#ifndef EXPAND_BINARY_LOGITS
template<size_t compilerBitPack>
class ApplyModelUpdateValidationInternal<2, compilerBitPack> final {
public:

   ApplyModelUpdateValidationInternal() = delete; // this is a static class.  Do not construct

   static FloatEbmType Func(
      BoosterShell * const pBoosterShell,
      const FeatureGroup * const pFeatureGroup
   ) {
      BoosterCore * const pBoosterCore = pBoosterShell->GetBoosterCore();
      const FloatEbmType * const aModelFeatureGroupUpdateTensor = pBoosterShell->GetAccumulatedModelUpdate()->GetValuePointer();
      EBM_ASSERT(nullptr != aModelFeatureGroupUpdateTensor);

      const size_t runtimeBitPack = pFeatureGroup->GetBitPack();
      DataSetBoosting * const pValidationSet = pBoosterCore->GetValidationSet();
      const FloatEbmType * pWeight = pBoosterCore->GetValidationWeights();
#ifndef NDEBUG
      FloatEbmType weightTotalDebug = 0;
#endif // NDEBUG

      const size_t cSamples = pValidationSet->GetCountSamples();
      EBM_ASSERT(1 <= cSamples);
      EBM_ASSERT(1 <= pFeatureGroup->GetCountSignificantDimensions());

      const size_t cItemsPerBitPack = GET_ITEMS_PER_BIT_PACK(compilerBitPack, runtimeBitPack);
      EBM_ASSERT(1 <= cItemsPerBitPack);
      EBM_ASSERT(cItemsPerBitPack <= k_cBitsForStorageType);
      const size_t cBitsPerItemMax = GetCountBits(cItemsPerBitPack);
      EBM_ASSERT(1 <= cBitsPerItemMax);
      EBM_ASSERT(cBitsPerItemMax <= k_cBitsForStorageType);
      const size_t maskBits = std::numeric_limits<size_t>::max() >> (k_cBitsForStorageType - cBitsPerItemMax);

      FloatEbmType sumLogLoss = FloatEbmType { 0 };
      const StorageDataType * pInputData = pValidationSet->GetInputDataPointer(pFeatureGroup);
      const StorageDataType * pTargetData = pValidationSet->GetTargetDataPointer();
      FloatEbmType * pPredictorScores = pValidationSet->GetPredictorScores();

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
            // this will apply a small fix to our existing ValidationPredictorScores, either positive or negative, whichever is needed
            const FloatEbmType predictorScore = *pPredictorScores + smallChangeToPredictorScores;
            *pPredictorScores = predictorScore;
            ++pPredictorScores;
            const FloatEbmType sampleLogLoss = EbmStats::ComputeSingleSampleLogLossBinaryClassification(predictorScore, targetData);

            EBM_ASSERT(std::isnan(sampleLogLoss) || FloatEbmType { 0 } <= sampleLogLoss);

            FloatEbmType weight = FloatEbmType { 1 };
            if(nullptr != pWeight) {
               // TODO: template this check away
               weight = *pWeight;
               ++pWeight;
#ifndef NDEBUG
               weightTotalDebug += weight;
#endif // NDEBUG
            }
            sumLogLoss += sampleLogLoss * weight;

            iTensorBinCombined >>= cBitsPerItemMax;
         } while(pPredictorScoresInnerEnd != pPredictorScores);
      } while(pPredictorScoresExit != pPredictorScores);

      // first time through?
      if(pPredictorScoresTrueEnd != pPredictorScores) {
         pPredictorScoresInnerEnd = pPredictorScoresTrueEnd;
         pPredictorScoresExit = pPredictorScoresTrueEnd;
         goto one_last_loop;
      }
      const FloatEbmType totalWeight = pBoosterCore->GetValidationWeightTotal();

      EBM_ASSERT(FloatEbmType { 0 } < totalWeight);
      EBM_ASSERT(nullptr == pWeight || totalWeight * 0.999 <= weightTotalDebug &&
         weightTotalDebug <= 1.001 * totalWeight);
      EBM_ASSERT(nullptr != pWeight || static_cast<FloatEbmType>(cSamples) == totalWeight);

      return sumLogLoss / totalWeight;
   }
};
#endif // EXPAND_BINARY_LOGITS

template<size_t compilerBitPack>
class ApplyModelUpdateValidationInternal<k_regression, compilerBitPack> final {
public:

   ApplyModelUpdateValidationInternal() = delete; // this is a static class.  Do not construct

   static FloatEbmType Func(
      BoosterShell * const pBoosterShell,
      const FeatureGroup * const pFeatureGroup
   ) {
      BoosterCore * const pBoosterCore = pBoosterShell->GetBoosterCore();
      const FloatEbmType * const aModelFeatureGroupUpdateTensor = pBoosterShell->GetAccumulatedModelUpdate()->GetValuePointer();
      EBM_ASSERT(nullptr != aModelFeatureGroupUpdateTensor);

      const size_t runtimeBitPack = pFeatureGroup->GetBitPack();
      DataSetBoosting * const pValidationSet = pBoosterCore->GetValidationSet();
      const FloatEbmType * pWeight = pBoosterCore->GetValidationWeights();
#ifndef NDEBUG
      FloatEbmType weightTotalDebug = 0;
#endif // NDEBUG

      const size_t cSamples = pValidationSet->GetCountSamples();
      EBM_ASSERT(1 <= cSamples);
      EBM_ASSERT(1 <= pFeatureGroup->GetCountSignificantDimensions());

      const size_t cItemsPerBitPack = GET_ITEMS_PER_BIT_PACK(compilerBitPack, runtimeBitPack);
      EBM_ASSERT(1 <= cItemsPerBitPack);
      EBM_ASSERT(cItemsPerBitPack <= k_cBitsForStorageType);
      const size_t cBitsPerItemMax = GetCountBits(cItemsPerBitPack);
      EBM_ASSERT(1 <= cBitsPerItemMax);
      EBM_ASSERT(cBitsPerItemMax <= k_cBitsForStorageType);
      const size_t maskBits = std::numeric_limits<size_t>::max() >> (k_cBitsForStorageType - cBitsPerItemMax);

      FloatEbmType sumSquareError = FloatEbmType { 0 };
      // no hessians for regression
      FloatEbmType * pGradient = pValidationSet->GetGradientsAndHessiansPointer();
      const StorageDataType * pInputData = pValidationSet->GetInputDataPointer(pFeatureGroup);

      // this shouldn't overflow since we're accessing existing memory
      const FloatEbmType * const pGradientsTrueEnd = pGradient + cSamples;
      const FloatEbmType * pGradientsExit = pGradientsTrueEnd;
      const FloatEbmType * pGradientsInnerEnd = pGradientsTrueEnd;
      if(cSamples <= cItemsPerBitPack) {
         goto one_last_loop;
      }
      pGradientsExit = pGradientsTrueEnd - ((cSamples - 1) % cItemsPerBitPack + 1);
      EBM_ASSERT(pGradient < pGradientsExit);
      EBM_ASSERT(pGradientsExit < pGradientsTrueEnd);

      do {
         pGradientsInnerEnd = pGradient + cItemsPerBitPack;
         // jumping back into this loop and changing pPredictorScoresInnerEnd to a dynamic value that isn't compile time determinable causes this 
         // function to NOT be optimized for templated cItemsPerBitPack, but that's ok since avoiding one unpredictable branch here is negligible
      one_last_loop:;
         // we store the already multiplied dimensional value in *pInputData
         size_t iTensorBinCombined = static_cast<size_t>(*pInputData);
         ++pInputData;
         do {
            const size_t iTensorBin = maskBits & iTensorBinCombined;

            const FloatEbmType smallChangeToPrediction = aModelFeatureGroupUpdateTensor[iTensorBin];
            // this will apply a small fix to our existing ValidationPredictorScores, either positive or negative, whichever is needed
            const FloatEbmType gradient = EbmStats::ComputeGradientRegressionMSEFromOriginalGradient(*pGradient, smallChangeToPrediction);
            const FloatEbmType sampleSquaredError = EbmStats::ComputeSingleSampleSquaredErrorRegressionFromGradient(gradient);
            EBM_ASSERT(std::isnan(sampleSquaredError) || FloatEbmType { 0 } <= sampleSquaredError);

            FloatEbmType weight = FloatEbmType { 1 };
            if(nullptr != pWeight) {
               // TODO: template this check away
               weight = *pWeight;
               ++pWeight;
#ifndef NDEBUG
               weightTotalDebug += weight;
#endif // NDEBUG
            }
            sumSquareError += sampleSquaredError * weight;
            *pGradient = gradient;
            ++pGradient;

            iTensorBinCombined >>= cBitsPerItemMax;
         } while(pGradientsInnerEnd != pGradient);
      } while(pGradientsExit != pGradient);

      // first time through?
      if(pGradientsTrueEnd != pGradient) {
         pGradientsInnerEnd = pGradientsTrueEnd;
         pGradientsExit = pGradientsTrueEnd;
         goto one_last_loop;
      }
      const FloatEbmType totalWeight = pBoosterCore->GetValidationWeightTotal();

      EBM_ASSERT(FloatEbmType { 0 } < totalWeight);
      EBM_ASSERT(nullptr == pWeight || totalWeight * 0.999 <= weightTotalDebug &&
         weightTotalDebug <= 1.001 * totalWeight);
      EBM_ASSERT(nullptr != pWeight || static_cast<FloatEbmType>(cSamples) == totalWeight);

      return sumSquareError / totalWeight;
   }
};

template<ptrdiff_t compilerLearningTypeOrCountTargetClassesPossible>
class ApplyModelUpdateValidationNormalTarget final {
public:

   ApplyModelUpdateValidationNormalTarget() = delete; // this is a static class.  Do not construct

   INLINE_ALWAYS static FloatEbmType Func(
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
         return ApplyModelUpdateValidationInternal<compilerLearningTypeOrCountTargetClassesPossible, k_cItemsPerBitPackDynamic>::Func(
            pBoosterShell,
            pFeatureGroup
         );
      } else {
         return ApplyModelUpdateValidationNormalTarget<
            compilerLearningTypeOrCountTargetClassesPossible + 1
         >::Func(
            pBoosterShell,
            pFeatureGroup
         );
      }
   }
};

template<>
class ApplyModelUpdateValidationNormalTarget<k_cCompilerOptimizedTargetClassesMax + 1> final {
public:

   ApplyModelUpdateValidationNormalTarget() = delete; // this is a static class.  Do not construct

   INLINE_ALWAYS static FloatEbmType Func(
      BoosterShell * const pBoosterShell,
      const FeatureGroup * const pFeatureGroup
   ) {
      static_assert(IsClassification(k_cCompilerOptimizedTargetClassesMax), "k_cCompilerOptimizedTargetClassesMax needs to be a classification");

      EBM_ASSERT(IsClassification(pBoosterShell->GetBoosterCore()->GetRuntimeLearningTypeOrCountTargetClasses()));
      EBM_ASSERT(k_cCompilerOptimizedTargetClassesMax < pBoosterShell->GetBoosterCore()->GetRuntimeLearningTypeOrCountTargetClasses());

      return ApplyModelUpdateValidationInternal<k_dynamicClassification, k_cItemsPerBitPackDynamic>::Func(
         pBoosterShell,
         pFeatureGroup
      );
   }
};

template<ptrdiff_t compilerLearningTypeOrCountTargetClasses, size_t compilerBitPack>
class ApplyModelUpdateValidationSIMDPacking final {
public:

   ApplyModelUpdateValidationSIMDPacking() = delete; // this is a static class.  Do not construct

   INLINE_ALWAYS static FloatEbmType Func(
      BoosterShell * const pBoosterShell,
      const FeatureGroup * const pFeatureGroup
   ) {
      const size_t runtimeBitPack = pFeatureGroup->GetBitPack();

      EBM_ASSERT(1 <= runtimeBitPack);
      EBM_ASSERT(runtimeBitPack <= k_cBitsForStorageType);
      static_assert(compilerBitPack <= k_cBitsForStorageType, "We can't have this many items in a data pack.");
      if(compilerBitPack == runtimeBitPack) {
         return ApplyModelUpdateValidationInternal<compilerLearningTypeOrCountTargetClasses, compilerBitPack>::Func(
            pBoosterShell,
            pFeatureGroup
         );
      } else {
         return ApplyModelUpdateValidationSIMDPacking<
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
class ApplyModelUpdateValidationSIMDPacking<compilerLearningTypeOrCountTargetClasses, k_cItemsPerBitPackDynamic> final {
public:

   ApplyModelUpdateValidationSIMDPacking() = delete; // this is a static class.  Do not construct

   INLINE_ALWAYS static FloatEbmType Func(
      BoosterShell * const pBoosterShell,
      const FeatureGroup * const pFeatureGroup
   ) {
      EBM_ASSERT(1 <= pFeatureGroup->GetBitPack());
      EBM_ASSERT(pFeatureGroup->GetBitPack() <= static_cast<ptrdiff_t>(k_cBitsForStorageType));
      return ApplyModelUpdateValidationInternal<
         compilerLearningTypeOrCountTargetClasses, 
         k_cItemsPerBitPackDynamic
      >::Func(
         pBoosterShell,
         pFeatureGroup
      );
   }
};

template<ptrdiff_t compilerLearningTypeOrCountTargetClassesPossible>
class ApplyModelUpdateValidationSIMDTarget final {
public:

   ApplyModelUpdateValidationSIMDTarget() = delete; // this is a static class.  Do not construct

   INLINE_ALWAYS static FloatEbmType Func(
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
         return ApplyModelUpdateValidationSIMDPacking<
            compilerLearningTypeOrCountTargetClassesPossible,
            k_cItemsPerBitPackMax
         >::Func(
            pBoosterShell,
            pFeatureGroup
         );
      } else {
         return ApplyModelUpdateValidationSIMDTarget<
            compilerLearningTypeOrCountTargetClassesPossible + 1
         >::Func(
            pBoosterShell,
            pFeatureGroup
         );
      }
   }
};

template<>
class ApplyModelUpdateValidationSIMDTarget<k_cCompilerOptimizedTargetClassesMax + 1> final {
public:

   ApplyModelUpdateValidationSIMDTarget() = delete; // this is a static class.  Do not construct

   INLINE_ALWAYS static FloatEbmType Func(
      BoosterShell * const pBoosterShell,
      const FeatureGroup * const pFeatureGroup
   ) {
      static_assert(IsClassification(k_cCompilerOptimizedTargetClassesMax), "k_cCompilerOptimizedTargetClassesMax needs to be a classification");

      EBM_ASSERT(IsClassification(pBoosterShell->GetBoosterCore()->GetRuntimeLearningTypeOrCountTargetClasses()));
      EBM_ASSERT(k_cCompilerOptimizedTargetClassesMax < pBoosterShell->GetBoosterCore()->GetRuntimeLearningTypeOrCountTargetClasses());

      return ApplyModelUpdateValidationSIMDPacking<
         k_dynamicClassification,
         k_cItemsPerBitPackMax
      >::Func(
         pBoosterShell,
         pFeatureGroup
      );
   }
};

extern FloatEbmType ApplyModelUpdateValidation(
   BoosterShell * const pBoosterShell, 
   const FeatureGroup * const pFeatureGroup
) {
   LOG_0(TraceLevelVerbose, "Entered ApplyModelUpdateValidation");

   BoosterCore * const pBoosterCore = pBoosterShell->GetBoosterCore();
   const ptrdiff_t runtimeLearningTypeOrCountTargetClasses = pBoosterCore->GetRuntimeLearningTypeOrCountTargetClasses();

   FloatEbmType ret;
   if(0 == pFeatureGroup->GetCountSignificantDimensions()) {
      if(IsClassification(runtimeLearningTypeOrCountTargetClasses)) {
         ret = ApplyModelUpdateValidationZeroFeaturesTarget<2>::Func(pBoosterShell);
      } else {
         EBM_ASSERT(IsRegression(runtimeLearningTypeOrCountTargetClasses));
         ret = ApplyModelUpdateValidationZeroFeatures<k_regression>::Func(pBoosterShell);
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
            ret = ApplyModelUpdateValidationSIMDTarget<2>::Func(
               pBoosterShell,
               pFeatureGroup
            );
         } else {
            EBM_ASSERT(IsRegression(runtimeLearningTypeOrCountTargetClasses));
            ret = ApplyModelUpdateValidationSIMDPacking<k_regression, k_cItemsPerBitPackMax>::Func(
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
            ret = ApplyModelUpdateValidationNormalTarget<2>::Func(
               pBoosterShell,
               pFeatureGroup
            );
         } else {
            EBM_ASSERT(IsRegression(runtimeLearningTypeOrCountTargetClasses));
            ret = ApplyModelUpdateValidationInternal<k_regression, k_cItemsPerBitPackDynamic>::Func(
               pBoosterShell,
               pFeatureGroup
            );
         }
      }
   }

   EBM_ASSERT(std::isnan(ret) || -k_epsilonLogLoss <= ret);
   // comparing to max is a good way to check for +infinity without using infinity, which can be problematic on
   // some compilers with some compiler settings.  Using <= helps avoid optimization away because the compiler
   // might assume that nothing is larger than max if it thinks there's no +infinity
   if(UNLIKELY(UNLIKELY(std::isnan(ret)) || UNLIKELY(std::numeric_limits<FloatEbmType>::max() <= ret))) {
      // set the metric so high that this round of boosting will be rejected.  The worst metric is std::numeric_limits<FloatEbmType>::max(),
      // Set it to that so that this round of boosting won't be accepted if our caller is using early stopping
      ret = std::numeric_limits<FloatEbmType>::max();
   } else {
      if(IsClassification(runtimeLearningTypeOrCountTargetClasses)) {
         if(UNLIKELY(ret < FloatEbmType { 0 })) {
            // regression can't be negative since squares are pretty well insulated from ever doing that

            // Multiclass can return small negative numbers, so we need to clean up the value retunred so that it isn't negative

            // binary classification can't return a negative number provided the log function
            // doesn't ever return a negative number for numbers exactly equal to 1 or higher
            // BUT we're going to be using or trying approximate log functions, and those might not
            // be guaranteed to return a positive or zero number, so let's just always check for numbers less than zero and round up
            EBM_ASSERT(IsMulticlass(runtimeLearningTypeOrCountTargetClasses));

            // because of floating point inexact reasons, ComputeSingleSampleLogLossMulticlass can return a negative number
            // so correct this before we return.  Any negative numbers were really meant to be zero
            ret = FloatEbmType { 0 };
         }
      }
   }
   EBM_ASSERT(!std::isnan(ret));
   EBM_ASSERT(!std::isinf(ret));
   EBM_ASSERT(FloatEbmType { 0 } <= ret);

   LOG_0(TraceLevelVerbose, "Exited ApplyModelUpdateValidation");

   return ret;
}

} // DEFINED_ZONE_NAME
