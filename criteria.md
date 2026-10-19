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

I chose 72.5% because my project has four GRC categories, and I want the model to classify most discussions correctly. I think this is a reasonable starting target for a small dataset.

---

## 2. Per-Label F1 Score

**Target:** Every label must achieve an F1 score of at least 0.50
on the held-out test set.

**Why this target:**

I chose 0.50 because some GRC topics are similar, especially security risk and compliance. Since the model may confuse these categories, I want a realistic minimum score for each label.

---

## 3. Class Balance

**Target:** No single label should exceed 40% of the labeled dataset.

**Why this target:**

I chose 40% because I don't want one category to dominate my dataset. My project has four labels, and I want the model to learn from governance, security, compliance, and vendor risk discussions.

---

## 4. Labeling Consistency

**Target:** Two independent reviewers should agree on at least
90% of the posts they both label.

**Why this target:**

I chose 90% because I want different people to classify the same discussions in a similar way. Some posts can fit more than one GRC category, so clear labeling rules are important.

---

## 5. Prediction Confidence

**Target:** At least 80% of predictions made with confidence
above 77.5% should be correct on the held-out test set.

**Why this target:**

I chose 80% accuracy for predictions above 77.5% confidence because I want the model's confident predictions to be more reliable. This could help reduce the number of posts that need manual checking.

---

<!--
UNIT 6 — IMPORTANT

Do not delete or overwrite the original acceptance criteria.

If a criterion cannot be measured, add a revision underneath
the original criterion and explain why it was revised.

Do not lower a target simply because the model failed to meet it.

Unit 6 evaluates targets across three training seeds.
-->