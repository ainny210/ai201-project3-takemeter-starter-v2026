# Acceptance Criteria — TakeMeter

## Project Overview

TakeMeter is a text classification project focused on AI and
Technology Governance, Risk, and Compliance (GRC).

The classifier uses four categories:

1. ai_governance_policy
2. ai_security_risk
3. compliance_implementation
4. vendor_third_party_risk

These acceptance criteria define what successful performance
would look like before training the classifier.

---

## How I Selected My Criteria

| Criterion | How to Choose |
|---|---|
| Overall Accuracy | Decide how many out of 100 posts the classifier should correctly categorize. |
| Per-Label F1 Score | Choose the minimum acceptable F1 score for each of the four categories. |
| Class Balance | Decide the maximum percentage of examples belonging to one category. The assignment limit is 70%. |
| Labeling Consistency | Decide how frequently two independent reviewers should assign the same label. |
| Prediction Confidence | Decide the confidence threshold and the required accuracy of predictions above that threshold. |

---

## 1. Overall Accuracy

**Target:** At least [CHOOSE NUMBER]% accuracy on the held-out test set.

**Why this target:**

[Explain how many correct predictions out of 100 would make
the GRC classifier useful for organizing discussions.]

---

## 2. Per-Label F1 Score

**Target:** Every label must achieve an F1 score of at least [CHOOSE NUMBER].

**Why this target:**

[Explain why the classifier needs to recognize all four GRC
categories rather than performing well on only one category.]

---

## 3. Class Balance

**Target:** No single label should exceed [CHOOSE NUMBER]% of the dataset.

**Why this target:**

[Explain why sufficient examples are needed for governance,
security risk, compliance, and vendor risk.]

---

## 4. Labeling Consistency

**Target:** Two independent reviewers should agree on at least
[CHOOSE NUMBER]% of the same posts.

**Why this target:**

[Explain why different reviewers might disagree about whether
a discussion concerns security risk or compliance implementation.]

---

## 5. Prediction Confidence

**Target:** At least [CHOOSE NUMBER]% of predictions with confidence
above [CHOOSE NUMBER]% should be correct.

**Why this target:**

[Explain why high-confidence predictions should be more
reliable than uncertain predictions.]

---

<!--
UNIT 6 — IMPORTANT

Do not delete or overwrite the original acceptance criteria.

If a criterion cannot be measured, add a revision underneath
the original criterion and explain why it was revised.

Do not lower a target simply because the model failed to meet it.

Unit 6 evaluates the targets across three training seeds.
-->