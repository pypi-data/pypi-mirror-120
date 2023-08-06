// Copyright (c) 2018 Microsoft Corporation
// Licensed under the MIT license.
// Author: Paul Koch <code@koch.ninja>

#include "precompiled_header_test.hpp"

#include "ebm_native.h"
#include "ebm_native_test.hpp"

static const TestPriority k_filePriority = TestPriority::InteractionUnusualInputs;

TEST_CASE("null interactionScoreOut, interaction, regression") {
   InteractionHandle interactionHandle;
   const ErrorEbmType error = CreateRegressionInteractionDetector(0, nullptr, nullptr, 0, nullptr, nullptr, nullptr, nullptr, nullptr, &interactionHandle);
   CHECK(Error_None == error);
   const ErrorEbmType ret = CalculateInteractionScore(interactionHandle, 0, nullptr, k_countSamplesRequiredForChildSplitMinDefault, nullptr);
   CHECK(Error_None == ret);
   FreeInteractionDetector(interactionHandle);
}

TEST_CASE("null interactionScoreOut, interaction, binary") {
   InteractionHandle interactionHandle;
   const ErrorEbmType error = CreateClassificationInteractionDetector(2, 0, nullptr, nullptr, 0, nullptr, nullptr, nullptr, nullptr, nullptr, &interactionHandle);
   CHECK(Error_None == error);
   const ErrorEbmType ret = CalculateInteractionScore(interactionHandle, 0, nullptr, k_countSamplesRequiredForChildSplitMinDefault, nullptr);
   CHECK(Error_None == ret);
   FreeInteractionDetector(interactionHandle);
}

TEST_CASE("null interactionScoreOut, interaction, multiclass") {
   InteractionHandle interactionHandle;
   const ErrorEbmType error = CreateClassificationInteractionDetector(3, 0, nullptr, nullptr, 0, nullptr, nullptr, nullptr, nullptr, nullptr, &interactionHandle);
   CHECK(Error_None == error);
   const ErrorEbmType ret = CalculateInteractionScore(interactionHandle, 0, nullptr, k_countSamplesRequiredForChildSplitMinDefault, nullptr);
   CHECK(Error_None == ret);
   FreeInteractionDetector(interactionHandle);
}

TEST_CASE("Zero interaction samples, interaction, regression") {
   TestApi test = TestApi(k_learningTypeRegression);
   test.AddFeatures({ FeatureTest(2) });
   test.AddInteractionSamples({});
   test.InitializeInteraction();

   FloatEbmType metricReturn = test.InteractionScore({ 0 });
   CHECK(0 == metricReturn);
}

TEST_CASE("Zero interaction samples, interaction, binary") {
   TestApi test = TestApi(2, 0);
   test.AddFeatures({ FeatureTest(2) });
   test.AddInteractionSamples({});
   test.InitializeInteraction();

   FloatEbmType metricReturn = test.InteractionScore({ 0 });
   CHECK(0 == metricReturn);
}

TEST_CASE("Zero interaction samples, interaction, multiclass") {
   TestApi test = TestApi(3);
   test.AddFeatures({ FeatureTest(2) });
   test.AddInteractionSamples({});
   test.InitializeInteraction();

   FloatEbmType metricReturn = test.InteractionScore({ 0 });
   CHECK(0 == metricReturn);
}

TEST_CASE("classification with 0 possible target states, interaction") {
   TestApi test = TestApi(0);
   test.AddFeatures({ FeatureTest(2) });
   test.AddInteractionSamples({});
   test.InitializeInteraction();

   FloatEbmType validationMetric = test.InteractionScore({ 0 });
   CHECK(0 == validationMetric);
}

TEST_CASE("classification with 1 possible target, interaction") {
   TestApi test = TestApi(1);
   test.AddFeatures({ FeatureTest(2) });
   test.AddInteractionSamples({ TestSample({ 1 }, 0) });
   test.InitializeInteraction();

   FloatEbmType validationMetric = test.InteractionScore({ 0 });
   CHECK(0 == validationMetric);
}

TEST_CASE("features with 0 states, interaction") {
   TestApi test = TestApi(k_learningTypeRegression);
   test.AddFeatures({ FeatureTest(0) });
   test.AddInteractionSamples({});
   test.InitializeInteraction();

   FloatEbmType validationMetric = test.InteractionScore({ 0 });
   CHECK(0 == validationMetric);
}

TEST_CASE("FeatureGroup with zero features, interaction, regression") {
   TestApi test = TestApi(k_learningTypeRegression);
   test.AddFeatures({});
   test.AddInteractionSamples({ TestSample({}, 10) });
   test.InitializeInteraction();
   FloatEbmType metricReturn = test.InteractionScore({});
   CHECK(0 == metricReturn);
}

TEST_CASE("FeatureGroup with zero features, interaction, binary") {
   TestApi test = TestApi(2, 0);
   test.AddFeatures({});
   test.AddInteractionSamples({ TestSample({}, 0) });
   test.InitializeInteraction();
   FloatEbmType metricReturn = test.InteractionScore({});
   CHECK(0 == metricReturn);
}

TEST_CASE("FeatureGroup with zero features, interaction, multiclass") {
   TestApi test = TestApi(3);
   test.AddFeatures({});
   test.AddInteractionSamples({ TestSample({}, 0) });
   test.InitializeInteraction();
   FloatEbmType metricReturn = test.InteractionScore({});
   CHECK(0 == metricReturn);
}

TEST_CASE("FeatureGroup with one feature with one state, interaction, regression") {
   TestApi test = TestApi(k_learningTypeRegression);
   test.AddFeatures({ FeatureTest(1) });
   test.AddInteractionSamples({ TestSample({ 0 }, 10) });
   test.InitializeInteraction();
   FloatEbmType metricReturn = test.InteractionScore({ 0 });
   CHECK(0 == metricReturn);
}

TEST_CASE("FeatureGroup with one feature with one state, interaction, binary") {
   TestApi test = TestApi(2, 0);
   test.AddFeatures({ FeatureTest(1) });
   test.AddInteractionSamples({ TestSample({ 0 }, 0) });
   test.InitializeInteraction();
   FloatEbmType metricReturn = test.InteractionScore({ 0 });
   CHECK(0 == metricReturn);
}

TEST_CASE("FeatureGroup with one feature with one state, interaction, multiclass") {
   TestApi test = TestApi(3);
   test.AddFeatures({ FeatureTest(1) });
   test.AddInteractionSamples({ TestSample({ 0 }, 0) });
   test.InitializeInteraction();
   FloatEbmType metricReturn = test.InteractionScore({ 0 });
   CHECK(0 == metricReturn);
}

TEST_CASE("weights are proportional, interaction, regression") {
   TestApi test1 = TestApi(k_learningTypeRegression);
   test1.AddFeatures({ FeatureTest(2), FeatureTest(2) });
   test1.AddInteractionSamples({ 
      TestSample({ 0, 0 }, 10.1, std::nextafter(0.3, 100)),
      TestSample({ 0, 1 }, 20.2, 0.3),
      TestSample({ 1, 0 }, 30.3, 0.3),
      TestSample({ 1, 1 }, 40.4, 0.3),
      });
   test1.InitializeInteraction();
   FloatEbmType metricReturn1 = test1.InteractionScore({ 0, 1 });

   TestApi test2 = TestApi(k_learningTypeRegression);
   test2.AddFeatures({ FeatureTest(2), FeatureTest(2) });
   test2.AddInteractionSamples({
      TestSample({ 0, 0 }, 10.1, std::nextafter(2, 100)),
      TestSample({ 0, 1 }, 20.2, 2),
      TestSample({ 1, 0 }, 30.3, 2),
      TestSample({ 1, 1 }, 40.4, 2),
      });
   test2.InitializeInteraction();
   FloatEbmType metricReturn2 = test2.InteractionScore({ 0, 1 });

   TestApi test3 = TestApi(k_learningTypeRegression);
   test3.AddFeatures({ FeatureTest(2), FeatureTest(2) });
   test3.AddInteractionSamples({
      TestSample({ 0, 0 }, 10.1, 0),
      TestSample({ 0, 1 }, 20.2, 0),
      TestSample({ 1, 0 }, 30.3, 0),
      TestSample({ 1, 1 }, 40.4, 0),
      });
   test3.InitializeInteraction();
   FloatEbmType metricReturn3 = test3.InteractionScore({ 0, 1 });

   CHECK_APPROX(metricReturn1, metricReturn2);
   CHECK_APPROX(metricReturn1, metricReturn3);
}

TEST_CASE("weights are proportional, interaction, binary") {
   TestApi test1 = TestApi(2);
   test1.AddFeatures({ FeatureTest(2), FeatureTest(2) });
   test1.AddInteractionSamples({
      TestSample({ 0, 0 }, 0, std::nextafter(0.3, 100)),
      TestSample({ 0, 1 }, 1, 0.3),
      TestSample({ 1, 0 }, 1, 0.3),
      TestSample({ 1, 1 }, 0, 0.3),
      });
   test1.InitializeInteraction();
   FloatEbmType metricReturn1 = test1.InteractionScore({ 0, 1 });

   TestApi test2 = TestApi(2);
   test2.AddFeatures({ FeatureTest(2), FeatureTest(2) });
   test2.AddInteractionSamples({
      TestSample({ 0, 0 }, 0, std::nextafter(2, 100)),
      TestSample({ 0, 1 }, 1, 2),
      TestSample({ 1, 0 }, 1, 2),
      TestSample({ 1, 1 }, 0, 2),
      });
   test2.InitializeInteraction();
   FloatEbmType metricReturn2 = test2.InteractionScore({ 0, 1 });

   TestApi test3 = TestApi(2);
   test3.AddFeatures({ FeatureTest(2), FeatureTest(2) });
   test3.AddInteractionSamples({
      TestSample({ 0, 0 }, 0, 0),
      TestSample({ 0, 1 }, 1, 0),
      TestSample({ 1, 0 }, 1, 0),
      TestSample({ 1, 1 }, 0, 0),
      });
   test3.InitializeInteraction();
   FloatEbmType metricReturn3 = test3.InteractionScore({ 0, 1 });

   CHECK_APPROX(metricReturn1, metricReturn2);
   CHECK_APPROX(metricReturn1, metricReturn3);
}

TEST_CASE("weights are proportional, interaction, multiclass") {
   TestApi test1 = TestApi(3);
   test1.AddFeatures({ FeatureTest(2), FeatureTest(2) });
   test1.AddInteractionSamples({
      TestSample({ 0, 0 }, 0, std::nextafter(0.3, 100)),
      TestSample({ 0, 1 }, 1, 0.3),
      TestSample({ 1, 0 }, 2, 0.3),
      TestSample({ 1, 1 }, 0, 0.3),
      });
   test1.InitializeInteraction();
   FloatEbmType metricReturn1 = test1.InteractionScore({ 0, 1 });

   TestApi test2 = TestApi(3);
   test2.AddFeatures({ FeatureTest(2), FeatureTest(2) });
   test2.AddInteractionSamples({
      TestSample({ 0, 0 }, 0, std::nextafter(2, 100)),
      TestSample({ 0, 1 }, 1, 2),
      TestSample({ 1, 0 }, 2, 2),
      TestSample({ 1, 1 }, 0, 2),
      });
   test2.InitializeInteraction();
   FloatEbmType metricReturn2 = test2.InteractionScore({ 0, 1 });

   TestApi test3 = TestApi(3);
   test3.AddFeatures({ FeatureTest(2), FeatureTest(2) });
   test3.AddInteractionSamples({
      TestSample({ 0, 0 }, 0, 0),
      TestSample({ 0, 1 }, 1, 0),
      TestSample({ 1, 0 }, 2, 0),
      TestSample({ 1, 1 }, 0, 0),
      });
   test3.InitializeInteraction();
   FloatEbmType metricReturn3 = test3.InteractionScore({ 0, 1 });

   CHECK_APPROX(metricReturn1, metricReturn2);
   CHECK_APPROX(metricReturn1, metricReturn3);
}

TEST_CASE("weights totals equivalence, interaction, regression") {
   TestApi test1 = TestApi(k_learningTypeRegression);
   test1.AddFeatures({ FeatureTest(2), FeatureTest(2) });
   test1.AddInteractionSamples({
      TestSample({ 0, 0 }, 10.1, 0.15),
      TestSample({ 0, 0 }, 10.1, 0.15),
      TestSample({ 0, 1 }, 20.2, 0.3),
      TestSample({ 1, 0 }, 30.3, 0.3),
      TestSample({ 1, 1 }, 40.4, 0.3),
      });
   test1.InitializeInteraction();
   FloatEbmType metricReturn1 = test1.InteractionScore({ 0, 1 });

   TestApi test2 = TestApi(k_learningTypeRegression);
   test2.AddFeatures({ FeatureTest(2), FeatureTest(2) });
   test2.AddInteractionSamples({
      TestSample({ 0, 0 }, 10.1, 2),
      TestSample({ 0, 1 }, 20.2, 2),
      TestSample({ 1, 0 }, 30.3, 1),
      TestSample({ 1, 0 }, 30.3, 1),
      TestSample({ 1, 1 }, 40.4, 2),
      });
   test2.InitializeInteraction();
   FloatEbmType metricReturn2 = test2.InteractionScore({ 0, 1 });

   CHECK_APPROX(metricReturn1, metricReturn2);
}

TEST_CASE("weights totals equivalence, interaction, binary") {
   TestApi test1 = TestApi(2);
   test1.AddFeatures({ FeatureTest(2), FeatureTest(2) });
   test1.AddInteractionSamples({
      TestSample({ 0, 0 }, 0, 0.3),
      TestSample({ 0, 1 }, 1, 0.15),
      TestSample({ 0, 1 }, 1, 0.15),
      TestSample({ 1, 0 }, 1, 0.3),
      TestSample({ 1, 1 }, 0, 0.3),
      });
   test1.InitializeInteraction();
   FloatEbmType metricReturn1 = test1.InteractionScore({ 0, 1 });

   TestApi test2 = TestApi(2);
   test2.AddFeatures({ FeatureTest(2), FeatureTest(2) });
   test2.AddInteractionSamples({
      TestSample({ 0, 0 }, 0, 2),
      TestSample({ 0, 1 }, 1, 2),
      TestSample({ 1, 0 }, 1, 2),
      TestSample({ 1, 1 }, 0, 1),
      TestSample({ 1, 1 }, 0, 1),
      });
   test2.InitializeInteraction();
   FloatEbmType metricReturn2 = test2.InteractionScore({ 0, 1 });

   CHECK_APPROX(metricReturn1, metricReturn2);
}

TEST_CASE("weights totals equivalence, interaction, multiclass") {
   TestApi test1 = TestApi(3);
   test1.AddFeatures({ FeatureTest(2), FeatureTest(2) });
   test1.AddInteractionSamples({
      TestSample({ 0, 0 }, 0, 0.3),
      TestSample({ 0, 1 }, 1, 0.15),
      TestSample({ 0, 1 }, 1, 0.15),
      TestSample({ 1, 0 }, 2, 0.3),
      TestSample({ 1, 1 }, 0, 0.3),
      });
   test1.InitializeInteraction();
   FloatEbmType metricReturn1 = test1.InteractionScore({ 0, 1 });

   TestApi test2 = TestApi(3);
   test2.AddFeatures({ FeatureTest(2), FeatureTest(2) });
   test2.AddInteractionSamples({
      TestSample({ 0, 0 }, 0, 1),
      TestSample({ 0, 0 }, 0, 1),
      TestSample({ 0, 1 }, 1, 2),
      TestSample({ 1, 0 }, 2, 2),
      TestSample({ 1, 1 }, 0, 2),
      });
   test2.InitializeInteraction();
   FloatEbmType metricReturn2 = test2.InteractionScore({ 0, 1 });

   CHECK_APPROX(metricReturn1, metricReturn2);
}
