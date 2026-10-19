# Acceptance Criteria — TakeMeter

## Project Overview

TakeMeter is a text classification project focused on AI and
Technology Governance, Risk, and Compliance (GRC).

The classifier uses four categories:

1. ai_governance_policy
2. ai_security_risk
3. compliance_implementation
4. vendor_third_party_risk

These acceptance criteria were selected before model training.

---

## 1. Overall Accuracy

**Target:** At least 72.5% accuracy on the held-out test set.

**Why this target:**

[Write one sentence explaining why correctly classifying approximately
73 out of 100 GRC discussions would be useful for your project.]

---

## 2. Per-Label F1 Score

**Target:** Every label must achieve an F1 score of at least 0.50
on the held-out test set.

**Why this target:**

[Write one sentence explaining why you chose a relatively modest
minimum F1 score for all four GRC categories.]

---

## 3. Class Balance

**Target:** No single label should exceed 40% of the labeled dataset.

**Why this target:**

[Write one sentence explaining why you want sufficient examples
from governance, security risk, compliance, and vendor risk.]

---

## 4. Labeling Consistency

**Target:** Two independent reviewers should agree on at least
90% of the posts they both label.

**Why this target:**

[Write one sentence explaining why consistent labeling matters,
especially when security and compliance topics overlap.]

---

## 5. Prediction Confidence

**Target:** At least 80% of predictions made with confidence
above 77.5% should be correct on the held-out test set.

**Why this target:**

[Write one sentence explaining why you expect predictions
with higher confidence to be more reliable.]

---

<!--
UNIT 6 — IMPORTANT

Do not delete or overwrite the original acceptance criteria.

If a criterion cannot be measured, add a revision underneath
the original criterion and explain why it was revised.

Do not lower a target simply because the model failed to meet it.

Unit 6 evaluates targets across three training seeds.
-->