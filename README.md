# TakeMeter — AI & Technology GRC Discussion Classifier

## What This Does

TakeMeter is a machine learning text classification project focused on **AI and Technology Governance, Risk, and Compliance (GRC)**.

The project uses community discussions from Information Security Stack Exchange to investigate whether a fine-tuned DistilBERT model can classify security-related questions into four GRC categories.

The four categories are:

1. `ai_governance_policy`
2. `ai_security_risk`
3. `compliance_implementation`
4. `vendor_third_party_risk`

The project evaluates classification accuracy, macro F1, per-label F1, reproducibility across three random seeds, and performance relative to a zero-shot baseline.

The objective is not simply to train a classifier, but to evaluate whether its performance is reliable enough for the intended classification task.

---

# Unit 5 — The Build

## Label Taxonomy

### 1. AI Governance and Policy

**Label:** `ai_governance_policy`

Discussions involving organizational governance, information security policies, responsibilities, approvals, decision-making, and security oversight.

### 2. AI Security Risk

**Label:** `ai_security_risk`

Discussions primarily involving security threats, vulnerabilities, privacy risks, sensitive information exposure, data breaches, and technical security risks.

### 3. Compliance Implementation

**Label:** `compliance_implementation`

Discussions involving compliance frameworks, regulatory requirements, audits, evidence collection, implementation of security controls, and compliance assessments.

### 4. Vendor and Third-Party Risk

**Label:** `vendor_third_party_risk`

Discussions about evaluating suppliers, third-party security assurance, vendor assessments, contractual security requirements, and ongoing vendor monitoring.

## Real Community Post Examples

### AI Governance and Policy

1. Information Security Policy and Information Security Plan
   Security Stack Exchange question 80193

2. Writing an information security policy
   Security Stack Exchange question 95116

### AI Security Risk

1. What is the difference between a data leak and a data breach?
   Security Stack Exchange question 229388

2. Knowing when there has been a data breach from your database
   Security Stack Exchange question 79816

### Compliance Implementation

1. How do I measure compliance to information security policies?
   Security Stack Exchange question 194068

2. Any place where I can find some template or base documents for IT/Infosec Compliance?
   Security Stack Exchange question 8997

### Vendor and Third-Party Risk

1. How can Huawei (or any other telecom vendor) provide verifiable security assurance?
   Security Stack Exchange question 199398

2. How to get medical vendors to take security seriously?
   Security Stack Exchange question 244188

## The Hardest Boundary

**Labels:** `ai_security_risk` and `compliance_implementation`

These categories overlap because compliance requirements frequently involve security controls.

**Decision rule:**

* Questions primarily about threats, vulnerabilities, attacks, breaches, or exposure belong to `ai_security_risk`.
* Questions primarily about regulatory requirements, audit preparation, control documentation, or demonstrating compliance belong to `compliance_implementation`.
* When both topics appear, the primary question determines the label.

For example, a question about preventing unauthorized database access belongs to AI Security Risk, while a question about documenting database access controls for an audit belongs to Compliance Implementation.

This distinction is important because classification should reflect the discussion's main purpose rather than the presence of individual security-related keywords.

---

## The Dataset

The project collected **822 candidate discussions** from the Information Security Stack Exchange API.

An initial relevance review identified 21 potentially relevant discussions and excluded 11.

The current labeled dataset contains **20 manually labeled examples**.

### Label Distribution

| Label                       |  Count | Percentage |
| --------------------------- | -----: | ---------: |
| `ai_governance_policy`      |      8 |        40% |
| `compliance_implementation` |      7 |        35% |
| `vendor_third_party_risk`   |      3 |        15% |
| `ai_security_risk`          |      2 |        10% |
| **Total**                   | **20** |   **100%** |

The dataset is imbalanced. Governance and compliance discussions account for 75% of labeled examples.

The project has not yet reached the assignment's minimum requirement of 150 labeled examples.

Consequently, the evaluation should be treated as preliminary rather than evidence of production readiness.

Source permissions for model-training use also require further verification.

### Three Difficult Labeling Cases

**Case 1: How a risk assessment impacts information security policy?**

Possible labels:

* `ai_governance_policy`
* `ai_security_risk`

Selected label: `ai_governance_policy`

Reason: The primary focus is how risk assessment informs organizational policy, rather than a specific technical threat.

**Case 2: Advice needed regarding Information Security Policy — EI3PA requirements**

Possible labels:

* `ai_governance_policy`
* `compliance_implementation`

Selected label: `compliance_implementation`

Reason: Although the discussion involves security policy, its main purpose is satisfying compliance requirements.

**Case 3: How can Huawei (or any other telecom vendor) provide verifiable security assurance?**

Possible labels:

* `vendor_third_party_risk`
* `compliance_implementation`

Selected label: `vendor_third_party_risk`

Reason: The question focuses on evaluating the security assurance of an external supplier.

---

## The Training Run

### Model Configuration

| Setting                       | Value                                 |
| ----------------------------- | ------------------------------------- |
| Base model                    | `distilbert-base-uncased`             |
| Task                          | Four-class text classification        |
| Framework                     | PyTorch and Hugging Face Transformers |
| Device                        | CPU                                   |
| Learning rate                 | `2e-5`                                |
| Batch size                    | 16                                    |
| Maximum sequence length       | 128                                   |
| Initial training epochs       | 3                                     |
| Improvement experiment epochs | 5                                     |
| Evaluation seeds              | 42, 7, 2024                           |

### Dataset Splitting

For each seed, the 20 labeled examples were divided into:

| Split      | Examples |
| ---------- | -------: |
| Training   |       14 |
| Validation |        3 |
| Test       |        3 |

The dataset was too small to support the attempted stratified split with four classes and only three test examples.

Therefore, an unstratified split was used.

This is a significant evaluation limitation because some labels may not appear in a particular test split.

The seed-specific splits can also differ, meaning the observed variability reflects both training randomness and differences in the evaluated examples.

### Initial Training Results

The initial model was trained for three epochs.

For seed 42, the held-out test results were:

* Accuracy: **0.667**
* Macro F1: **0.400**

The initial evaluation demonstrated that the model could classify some held-out examples correctly, but performance varied substantially across seeds.

---

# Unit 6 — Testing

## Baseline vs. Trained

A zero-shot classification baseline was evaluated using `facebook/bart-large-mnli`.

The baseline used CPU execution with float16 model weights because loading the model at the original precision caused a memory-related error.

The baseline and initial trained model were evaluated on the same three held-out examples for seed 42.

### Results

| Measure                          | Zero-Shot Baseline | Trained DistilBERT | Difference |
| -------------------------------- | -----------------: | -----------------: | ---------: |
| Overall accuracy                 |              0.000 |              0.667 |     +0.667 |
| Macro F1                         |              0.000 |              0.400 |     +0.400 |
| F1 — `ai_governance_policy`      |              0.000 |              0.800 |     +0.800 |
| F1 — `ai_security_risk`          |              0.000 |              0.000 |      0.000 |
| F1 — `compliance_implementation` |              0.000 |              0.000 |      0.000 |
| F1 — `vendor_third_party_risk`   |              0.000 |              0.000 |      0.000 |

### What I Predicted Before Looking

A prediction was not documented before examining the results, so no retrospective prediction is presented as precommitted evidence.

### What the Gap Actually Means

The fine-tuned DistilBERT model outperformed the zero-shot baseline on the seed 42 test split.

However, the improvement was concentrated in the governance category.

The trained model did not demonstrate successful classification across all four categories.

Because the test split contained only three examples, the observed accuracy difference is not sufficient to establish that the trained model consistently outperforms the baseline.

The baseline also used float16 weights, which is an additional implementation difference worth noting.

---

## Run Log — Before

The original experiment trained the classifier for **three epochs** using seeds 42, 7, and 2024.

### Three-Seed Results

| Seed     | Test Accuracy |  Macro F1 |
| -------- | ------------: | --------: |
| 42       |         0.667 |     0.400 |
| 7        |         0.000 |     0.000 |
| 2024     |         0.333 |     0.250 |
| **Mean** |     **0.333** | **0.217** |

### Stability Analysis

The accuracy varied from 0.000 to 0.667 across the three seeds.

**Accuracy spread: 0.667 (66.7 percentage points).**

This large spread indicates that performance is unstable under the current training and evaluation procedure.

The small dataset and changing test splits make the results especially sensitive to individual examples.

### Per-Label F1

| Label                       | Seed 42 | Seed 7 | Seed 2024 |
| --------------------------- | ------: | -----: | --------: |
| `ai_governance_policy`      |   0.800 |  0.000 |     0.000 |
| `ai_security_risk`          |   0.000 |  0.000 |     0.000 |
| `compliance_implementation` |   0.000 |  0.000 |     0.500 |
| `vendor_third_party_risk`   |   0.000 |  0.000 |     0.000 |

The results show that successful classification is inconsistent across labels and seeds.

A zero F1 score should be interpreted carefully when a class has no support in a particular test split.

### Confusion Matrix

A verified confusion-matrix table has not been included because the exact true-label/predicted-label counts were not available in the recorded summary.

The underlying evaluation artifacts should be used to reconstruct the matrix rather than inventing counts.

**Largest off-diagonal error:** Not established from the available summary.

This prevents a defensible claim about which specific label boundary produced the largest number of errors.

---

## Verdicts and Diagnoses

The following verdicts use the original acceptance criteria. The targets have not been lowered after observing the results.

| # | Criterion                           | Original Target                            | Verdict          | Evidence                                                       |
| - | ----------------------------------- | ------------------------------------------ | ---------------- | -------------------------------------------------------------- |
| 1 | Held-out accuracy                   | At least 72.5% for every seed              | **MISSED**       | Accuracies were 66.7%, 0%, and 33.3%                           |
| 2 | Per-label held-out F1               | At least 0.50 for every label across seeds | **MISSED**       | Multiple categories had F1 of 0                                |
| 3 | Label distribution                  | No category above 40%                      | **MET**          | Largest category represents exactly 40%                        |
| 4 | Independent reviewer agreement      | At least 90%                               | **NOT MEASURED** | Independent review and agreement results are not available     |
| 5 | High-confidence prediction accuracy | At least 80% when confidence exceeds 77.5% | **NOT MEASURED** | Required confidence-filtered results have not been established |

### Criterion 1 — Accuracy

**Verdict: MISSED**

None of the three seeds achieved the required 72.5% accuracy.

Seed 42 achieved the highest accuracy at 66.7%.

Seed 7 achieved 0% accuracy.

The large difference between seeds indicates poor stability.

**Diagnosis:** The training dataset is too small to support reliable generalization, and the three-example test sets produce coarse and unstable accuracy estimates.

**Recommended revision:** Increase the number of labeled examples and use larger, class-representative evaluation splits.

### Criterion 2 — Per-Label F1

**Verdict: MISSED**

Several categories achieved an F1 score of zero.

The model performed best on governance-related examples in seed 42.

The minority categories have very limited training representation.

**Diagnosis:** Class imbalance and insufficient examples likely contribute to poor category coverage.

The current results do not establish whether all errors arise from inconsistent human labels or from model learning limitations.

**Recommended revision:** Expand minority-class examples and review ambiguous label boundaries before retraining.

### Criterion 3 — Class Distribution

**Verdict: MET**

The largest category, `ai_governance_policy`, represents 40% of the dataset.

This satisfies the stated requirement that no class exceed 40%.

However, satisfying this numerical threshold does not mean the dataset is sufficiently balanced for reliable model training.

### Criterion 4 — Reviewer Agreement

**Verdict: NOT MEASURED**

The required independent labeling comparison has not been completed.

Without agreement results, it is not possible to determine whether the label definitions are being applied consistently by different reviewers.

**Recommended revision:** Complete the staff taxonomy labeling exercise, calculate agreement, and adjudicate disagreements using the written taxonomy rules.

### Criterion 5 — High-Confidence Accuracy

**Verdict: NOT MEASURED**

The required accuracy calculation for predictions above 77.5% confidence has not been established.

Overall accuracy cannot be substituted for confidence-filtered accuracy.

**Recommended revision:** Save prediction probabilities, filter predictions above the original confidence threshold, and calculate accuracy on that subset.

---

## Diagnoses

### Diagnosis 1 — Insufficient Labeled Data

The strongest limitation is the size of the labeled dataset.

Only 20 examples are available for four classes.

Each training split contains 14 examples, leaving very little evidence from which the model can learn category-specific distinctions.

This is consistent with the unstable three-seed results.

### Diagnosis 2 — Minority-Class Representation

The dataset contains only:

* 2 examples of `ai_security_risk`
* 3 examples of `vendor_third_party_risk`

These categories are substantially underrepresented.

A classifier trained on so few examples may fail to recognize the linguistic patterns associated with these labels.

### Diagnosis 3 — Difficult Label Boundaries

Governance, security risk, and compliance frequently overlap.

For example, a discussion about security policy may focus on governance responsibilities, implementation of regulatory controls, or a specific security risk.

The taxonomy uses the primary purpose of the question as its decision rule, but agreement testing is still needed to determine whether different reviewers apply that rule consistently.

### Diagnosis 4 — Unstable Evaluation

With only three test examples, one changed prediction can alter accuracy by approximately 33.3 percentage points.

Therefore, a difference between seeds may be caused by a very small number of examples.

The unstratified splitting procedure also allows class representation to vary across test sets.

### Diagnosis 5 — Training Duration Alone May Not Be the Main Problem

The initial model used three epochs.

Additional training might help if the model had not received enough optimization steps.

However, the improvement experiment showed that increasing the number of epochs did not change held-out accuracy or macro F1.

This suggests that simply training longer is insufficient under the current data conditions.

---

## Agreement Report

**Agreement rate:** Not measured.

The required staff agreement exercise has not been completed.

The project has not yet produced a verified `agreement_results.json` containing a comparison between independently assigned labels and the staff reference labels.

### Disagreements

No staff disagreements have been adjudicated.

It would be misleading to report an agreement percentage or disagreement explanations without the actual comparison.

### What This Means for the Diagnosis

The model's poor performance is documented, but the available evidence cannot fully distinguish between:

1. Inconsistent human labeling.
2. Ambiguous taxonomy definitions.
3. Insufficient training data.
4. Model generalization failure.

A completed agreement report is necessary to investigate these possibilities more confidently.

---

## The Improvement

### Hypothesis

Increasing the number of training epochs from three to five might improve model performance by providing additional opportunities to learn from the labeled examples.

### What I Changed

The number of training epochs was increased:

**Before:** `EPOCHS = 3`

**After:** `EPOCHS = 5`

The following settings were retained:

* Base model: `distilbert-base-uncased`
* Learning rate: `2e-5`
* Batch size: 16
* Maximum sequence length: 128
* Seeds: 42, 7, 2024
* Dataset and label taxonomy
* Evaluation procedure

The experiment was saved separately as:

`results_three_seeds_after.json`

This preserves the original results in:

`results_three_seeds_before.json`

### Which Diagnosis Pointed at It?

The initial results showed low and inconsistent accuracy.

One possible explanation was insufficient training duration.

Increasing the epochs provided a direct test of whether additional optimization would improve performance.

This change did not directly address the separate problems of dataset size and class imbalance.

---

## Run Log — After

The updated experiment trained the model for **five epochs** using the same three seeds.

### Three-Seed Results

| Seed     | Test Accuracy |  Macro F1 |
| -------- | ------------: | --------: |
| 42       |         0.667 |     0.400 |
| 7        |         0.000 |     0.000 |
| 2024     |         0.333 |     0.250 |
| **Mean** |     **0.333** | **0.217** |

### Before vs. After Comparison

| Seed     | Before Accuracy | After Accuracy | Before Macro F1 | After Macro F1 |
| -------- | --------------: | -------------: | --------------: | -------------: |
| 42       |           0.667 |          0.667 |           0.400 |          0.400 |
| 7        |           0.000 |          0.000 |           0.000 |          0.000 |
| 2024     |           0.333 |          0.333 |           0.250 |          0.250 |
| **Mean** |       **0.333** |      **0.333** |       **0.217** |      **0.217** |

### Change in Performance

| Metric          | Before | After | Change |
| --------------- | -----: | ----: | -----: |
| Mean accuracy   |  0.333 | 0.333 |  0.000 |
| Mean macro F1   |  0.217 | 0.217 |  0.000 |
| Accuracy spread |  0.667 | 0.667 |  0.000 |

### Did It Help?

**No.**

Increasing the training duration from three to five epochs did not improve held-out accuracy or macro F1 for any of the three seeds.

The experiment therefore did not support the hypothesis that additional training epochs alone would improve the model.

This is a meaningful negative result because it narrows the likely next steps.

The evidence suggests that increasing labeled-data coverage and improving evaluation reliability should take priority over simply extending training.

### Acceptance Criteria After Improvement

| # | Criterion                | Target                                | After Verdict    |
| - | ------------------------ | ------------------------------------- | ---------------- |
| 1 | Held-out accuracy        | At least 72.5% across seeds           | **MISSED**       |
| 2 | Per-label F1             | At least 0.50 across labels and seeds | **MISSED**       |
| 3 | Maximum class proportion | No class above 40%                    | **MET**          |
| 4 | Reviewer agreement       | At least 90%                          | **NOT MEASURED** |
| 5 | High-confidence accuracy | At least 80% above 77.5% confidence   | **NOT MEASURED** |

No original acceptance threshold was changed.

---

## What's Still Broken

### 1. Dataset Size

The project currently contains 20 labeled examples rather than the required minimum of 150.

**Next step:** Continue manually labeling candidate discussions and prioritize coverage of underrepresented categories.

### 2. Class Imbalance

The security risk and vendor risk categories contain very few examples.

**Next step:** Expand minority categories and reassess label proportions.

### 3. Low Accuracy

The best seed achieved only 66.7% accuracy.

The three-seed mean accuracy was 33.3%.

**Next step:** Retrain using a larger labeled dataset and evaluate on a larger test set.

### 4. Low Per-Label F1

Several categories achieved zero F1.

**Next step:** Inspect individual false positives and false negatives, especially between overlapping GRC categories.

### 5. Missing Reviewer Agreement

The staff labeling and adjudication exercise is incomplete.

**Next step:** Label the 30 staff examples using the staff taxonomy, calculate agreement, and document every disagreement.

### 6. Missing Confidence Analysis

The high-confidence acceptance criterion has not been evaluated.

**Next step:** Export prediction probabilities and evaluate predictions above the original 77.5% confidence threshold.

### 7. Evaluation Reliability

Each seed currently evaluates only three held-out examples.

**Next step:** Increase test-set size and use class-representative splits where feasible.

### 8. Confusion Matrix Documentation

The exact confusion-matrix counts have not been included in this report.

**Next step:** Extract the matrix from the saved predictions and include it as a Markdown table.

### The Gap Between Intended Labels and Learned Behavior

The taxonomy is designed to distinguish four different types of GRC discussions.

However, the model has not demonstrated reliable recognition of all four categories.

The available results suggest that the model is learning some governance-related patterns while failing to generalize consistently across the remaining categories.

The current evidence is insufficient to determine the exact contribution of taxonomy ambiguity versus limited training data.

---

## How I Used AI

AI assistance was used to support development and documentation of this project.

Activities included:

1. Developing the data collection workflow and Python commands.
2. Reviewing the relevance of selected community discussions.
3. Structuring the four-category GRC taxonomy.
4. Troubleshooting notebook execution and Python errors.
5. Investigating model-loading memory errors.
6. Supporting the implementation of the zero-shot baseline.
7. Organizing the three-seed evaluation workflow.
8. Interpreting accuracy and macro F1 results.
9. Preparing the before-and-after comparison.
10. Structuring the final project documentation.

The reported evaluation numbers come from the executed experiments rather than AI-generated estimates.

Uncompleted measurements are identified explicitly instead of being presented as completed work.

---

## Reproducibility

### Project Files

| File                              | Purpose                             |
| --------------------------------- | ----------------------------------- |
| `takemeter.ipynb`                 | Training and evaluation notebook    |
| `labels.csv`                      | Manually labeled GRC discussions    |
| `label_definitions.txt`           | Label descriptions                  |
| `criteria.md`                     | Original acceptance criteria        |
| `baseline.py`                     | Zero-shot baseline evaluation       |
| `baseline_results.json`           | Baseline evaluation results         |
| `results.json`                    | Initial trained-model evaluation    |
| `test_split.csv`                  | Saved initial test split            |
| `results_three_seeds_before.json` | Three-seed evaluation with 3 epochs |
| `results_three_seeds_after.json`  | Three-seed evaluation with 5 epochs |
| `RUNNING.md`                      | Setup and execution instructions    |

### How to Run

Follow the environment setup instructions in `RUNNING.md`.

Run the notebook cells in order to define the dataset, splitting functions, training function, and evaluation function.

For the initial experiment:

```python
EPOCHS = 3
SEEDS = [42, 7, 2024]
RUN_LABEL = "before"
```

For the improvement experiment:

```python
EPOCHS = 5
SEEDS = [42, 7, 2024]
RUN_LABEL = "after"
```

Run the zero-shot baseline with:

```bash
python baseline.py
```

The notebook and scripts save evaluation results as JSON files for later comparison.

---

## Final Conclusion

This project investigated whether a fine-tuned DistilBERT model could classify information security community discussions into four AI and Technology GRC categories.

The initial three-seed experiment achieved:

* Mean accuracy: **33.3%**
* Mean macro F1: **0.217**

The five-epoch improvement experiment produced identical held-out metrics.

The zero-shot baseline achieved 0% accuracy on the three-example seed 42 test split, compared with 66.7% for the fine-tuned model.

However, the results remain unstable and do not satisfy the original accuracy and per-label F1 acceptance criteria.

The most important limitations are the small labeled dataset, uneven category representation, and very small test splits.

**The main finding is that additional training epochs did not improve performance under the current data conditions.**

Future development should prioritize more labeled examples, stronger class coverage, reviewer agreement testing, and larger evaluation sets before considering the classifier reliable for practical GRC applications.

---

**Project repository:** https://github.com/ainny210/ai201-project3-takemeter-starter-v2026

**Setup instructions:** [RUNNING.md](RUNNING.md)
