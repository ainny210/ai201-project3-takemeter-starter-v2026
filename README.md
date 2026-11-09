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

The objective is not simply to train a classifier but to evaluate whether its performance is reliable enough for the intended classification task.

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

1. Information Security Policy and Information Security Plan — Security Stack Exchange question 80193.
2. Writing an information security policy — Security Stack Exchange question 95116.

### AI Security Risk

1. What is the difference between a data leak and a data breach? — Security Stack Exchange question 229388.
2. Knowing when there has been a data breach from your database — Security Stack Exchange question 79816.

### Compliance Implementation

1. How do I measure compliance to information security policies? — Security Stack Exchange question 194068.
2. Any place where I can find some template or base documents for IT/Infosec Compliance? — Security Stack Exchange question 8997.

### Vendor and Third-Party Risk

1. How can Huawei (or any other telecom vendor) provide verifiable security assurance? — Security Stack Exchange question 199398.
2. How to get medical vendors to take security seriously? — Security Stack Exchange question 244188.

## The Hardest Boundary

**Labels:** `ai_security_risk` and `compliance_implementation`

These categories overlap because compliance requirements frequently involve security controls.

**Decision rule:**

* Questions primarily about threats, vulnerabilities, attacks, breaches, or exposure belong to `ai_security_risk`.
* Questions primarily about regulatory requirements, audit preparation, control documentation, or demonstrating compliance belong to `compliance_implementation`.
* When both topics appear, the primary question determines the label.

For example, a question about preventing unauthorized database access belongs to AI Security Risk, while a question about documenting database access controls for an audit belongs to Compliance Implementation.

This distinction is important because classification should reflect the discussion's main purpose rather than individual security-related keywords.

---

## The Dataset

The project collected **822 candidate discussions** from the Information Security Stack Exchange API.

An initial relevance review identified 21 potentially relevant discussions and excluded 11.

The current GRC dataset contains **20 manually labeled examples**.

### Label Distribution

| Label                       |  Count | Percentage |
| --------------------------- | -----: | ---------: |
| `ai_governance_policy`      |      8 |        40% |
| `compliance_implementation` |      7 |        35% |
| `vendor_third_party_risk`   |      3 |        15% |
| `ai_security_risk`          |      2 |        10% |
| **Total**                   | **20** |   **100%** |

The dataset is imbalanced. Governance and compliance discussions account for 75% of labeled examples.

**Dataset limitation:** The project has not reached the assignment's minimum requirement of 150 labeled GRC examples.

The evaluation should therefore be treated as preliminary rather than evidence of production readiness.

Source permissions for model-training use also require further verification.

### Three Difficult Labeling Cases

**Case 1: How a risk assessment impacts information security policy?**

Possible labels:

* `ai_governance_policy`
* `ai_security_risk`

**Selected label:** `ai_governance_policy`

**Reason:** The primary focus is how risk assessment informs organizational policy rather than a specific technical threat.

**Case 2: Advice needed regarding Information Security Policy — EI3PA requirements**

Possible labels:

* `ai_governance_policy`
* `compliance_implementation`

**Selected label:** `compliance_implementation`

**Reason:** Although the discussion involves security policy, its main purpose is satisfying compliance requirements.

**Case 3: How can Huawei (or any other telecom vendor) provide verifiable security assurance?**

Possible labels:

* `vendor_third_party_risk`
* `compliance_implementation`

**Selected label:** `vendor_third_party_risk`

**Reason:** The question focuses on evaluating the security assurance of an external supplier.

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

* **Accuracy:** 0.667
* **Macro F1:** 0.400

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

The following confusion matrix was generated from the initial trained DistilBERT model using seed 42 and three held-out test examples.

Rows represent actual labels, and columns represent predicted labels.

| Actual / Predicted | AI Governance | AI Security Risk | Compliance | Vendor Risk |
| ------------------ | ------------: | ---------------: | ---------: | ----------: |
| AI Governance      |             2 |                0 |          0 |           0 |
| AI Security Risk   |             0 |                0 |          0 |           0 |
| Compliance         |             0 |                0 |          0 |           0 |
| Vendor Risk        |             1 |                0 |          0 |           0 |

**Total test examples:** 3

**Correct predictions:** 2

**Incorrect predictions:** 1

**Accuracy:** 66.7%

#### Largest Off-Diagonal Error

The largest off-diagonal value is **1**, representing a `vendor_third_party_risk` discussion incorrectly classified as `ai_governance_policy`.

This indicates that the model failed to distinguish vendor security oversight from broader organizational governance in this example.

Both categories can involve policies, responsibilities, and security assurance. However, the taxonomy specifies that discussions primarily evaluating external suppliers belong to `vendor_third_party_risk`.

The model instead predicted `ai_governance_policy`.

#### What This Error Suggests

The model correctly classified both governance examples but failed to recognize the vendor-risk example.

This is consistent with the dataset imbalance:

* AI Governance: 8 labeled examples.
* Vendor Risk: 3 labeled examples.

The small number of vendor-risk training examples may have contributed to this error, although one misclassification cannot establish its exact cause.

Neither AI Security Risk nor Compliance Implementation appeared in this particular test split. Therefore, their zero confusion-matrix rows do not demonstrate successful or unsuccessful classification of those categories.

**Conclusion:** The confusion matrix provides evidence of a governance-versus-vendor-risk classification error. A larger and more representative test set is necessary to determine whether this error pattern is systematic.

---

## Verdicts and Diagnoses

The following verdicts use the original acceptance criteria. The targets have not been lowered after observing the results.

| # | Criterion                           | Original Target                            | Verdict                   | Evidence                                        |
| - | ----------------------------------- | ------------------------------------------ | ------------------------- | ----------------------------------------------- |
| 1 | Held-out accuracy                   | At least 72.5% for every seed              | **MISSED**                | Accuracies were 66.7%, 0%, and 33.3%            |
| 2 | Per-label held-out F1               | At least 0.50 for every label across seeds | **MISSED**                | Multiple categories had F1 of 0                 |
| 3 | Label distribution                  | No category above 40%                      | **MET**                   | Largest category represents exactly 40%         |
| 4 | Independent reviewer agreement      | At least 90%                               | **MET ON STAFF EXERCISE** | 30/30 staff-label matches; 100% agreement       |
| 5 | High-confidence prediction accuracy | At least 80% when confidence exceeds 77.5% | **NOT ESTABLISHED**       | Confidence-filtered accuracy was not calculated |

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

**Verdict: MET ON THE STAFF-LABELING EXERCISE**

I completed the separate staff taxonomy evaluation involving 30 posts.

The staff taxonomy contained three categories:

* `analysis`
* `hot_take`
* `reaction`

After labeling the posts, I compared my annotations with the official staff labels using `agreement.py`.

The comparison produced:

* **Posts compared:** 30
* **Agreements:** 30
* **Disagreements:** 0
* **Agreement rate:** 100%

The result exceeds the original 90% agreement threshold when applied to the staff exercise.

**Important distinction:** This evaluation used the staff's running-discussion taxonomy rather than the project's four-category GRC taxonomy. Therefore, it demonstrates agreement with the staff labels on the supplied exercise but does not establish independent reviewer agreement for the 20 GRC examples.

**Recommended revision:** Conduct a separate independent labeling review of the GRC dataset when more labeled examples are available.

### Criterion 5 — High-Confidence Accuracy

**Verdict: NOT ESTABLISHED**

The original criterion required at least 80% accuracy for predictions with confidence greater than 77.5%.

The saved evaluation produced the following confidence statistics:

| Metric                                        |   Result |
| --------------------------------------------- | -------: |
| Mean confidence when prediction was correct   | 0.264373 |
| Mean confidence when prediction was incorrect | 0.264172 |
| Accuracy of most confident third              |    1.000 |
| Accuracy of least confident third             |    1.000 |
| Examples per confidence third                 |        1 |

These results show that the model assigned similarly low average confidence to correct and incorrect predictions.

However, the accuracy of the most confident third is not equivalent to accuracy above the predefined 77.5% threshold.

The saved summary does not identify the number of predictions exceeding 77.5% confidence.

Therefore, the original confidence-filtered acceptance criterion cannot be conclusively evaluated from these summary statistics.

**Recommended revision:** Save the confidence of every held-out prediction, filter predictions with confidence greater than 0.775, and calculate accuracy on the qualifying subset. If no predictions qualify, report the subset as empty rather than claiming that the threshold was met.

---

## Diagnoses

### Diagnosis 1 — Insufficient Labeled Data

The strongest limitation is the size of the labeled dataset.

Only 20 examples are available for four classes.

Each training split contains 14 examples, leaving very little evidence from which the model can learn category-specific distinctions.

This is consistent with the unstable three-seed results.

### Diagnosis 2 — Minority-Class Representation

The dataset contains only:

* 2 examples of `ai_security_risk`.
* 3 examples of `vendor_third_party_risk`.

These categories are substantially underrepresented.

A classifier trained on so few examples may fail to recognize the linguistic patterns associated with these labels.

### Diagnosis 3 — Difficult Label Boundaries

Governance, security risk, and compliance frequently overlap.

For example, a discussion about security policy may focus on governance responsibilities, implementation of regulatory controls, or a specific security risk.

The taxonomy uses the primary purpose of the question as its decision rule.

The separate staff-labeling exercise achieved 100% agreement, but it used a different taxonomy. It therefore cannot resolve whether independent reviewers would consistently apply the project's GRC-specific label definitions.

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

### Staff Taxonomy Evaluation

I completed the staff-labeling exercise using the supplied taxonomy and decision rules.

The evaluation required labeling 30 fictional running-forum posts into three categories:

| Label      | Definition                                                                           |
| ---------- | ------------------------------------------------------------------------------------ |
| `analysis` | An argument supported by a specific, checkable fact that contributes to the argument |
| `hot_take` | A confident general claim without supporting evidence                                |
| `reaction` | An immediate personal response to a recent event or experience                       |

The taxonomy also provided rules for resolving ambiguous cases.

The key distinctions were:

1. A numerical fact makes a post `analysis` only when the fact supports the argument.
2. A personal emotional response is generally `reaction`, while an unsupported general claim is `hot_take`.
3. A recent event does not automatically make a post `reaction` when the post contains an evidence-supported argument.
4. When two labels remain defensible, the dominant purpose of the post determines the label.

### My Label Distribution

| Label      |  Count |
| ---------- | -----: |
| `analysis` |     10 |
| `hot_take` |     10 |
| `reaction` |     10 |
| **Total**  | **30** |

### Agreement Results

After completing the labeling exercise, I compared my labels with the official staff reference using:

`python agreement.py`

The script generated `agreement_results.json`.

The verified results were:

| Metric                             |   Result |
| ---------------------------------- | -------: |
| Posts compared                     |       30 |
| Agreements                         |       30 |
| Disagreements                      |        0 |
| Agreement rate                     | **100%** |
| Staff posts missing from my labels |        0 |

The JSON output was:

```json
{
  "compared": 30,
  "agreed": 30,
  "agreement_rate": 1.0,
  "disagreements": [],
  "staff_posts_not_in_mine": 0
}
```

### Interpretation

The results demonstrate that my annotations matched the official staff labels for all 30 supplied examples.

The distinction between evidence-supported arguments, unsupported general claims, and immediate personal reactions was useful when applying the taxonomy.

Some posts required closer attention because they included numbers or factual details without necessarily being evidence-supported arguments.

For example:

**Post `sp_014`:**

"Times are down about 3% since the shoe rules changed, so obviously the shoes are the whole story and the sport has a problem."

**Assigned label:** `hot_take`

Although the post includes a statistic, it makes a broad causal claim without demonstrating that the shoes alone caused the change. The statistic functions more as support for a predetermined opinion than as a developed argument.

**Post `sp_027`:**

"Wind was so bad on the out section I was leaning at about 20 degrees. Coming back felt like cheating."

**Assigned label:** `reaction`

The post contains a numerical detail, but its primary purpose is to describe a recent personal experience rather than make an evidence-supported general argument.

**Post `sp_029`:**

"Just realised the shoes I set every PB in this year are the ones I bought by accident in the wrong size."

**Assigned label:** `reaction`

The post primarily expresses an immediate personal realization. It does not use the observation to develop a broader argument.

### Disagreement Adjudication

The agreement script reported:

**Disagreements: 0**

Therefore, no disagreements required adjudication.

The exercise instructions identified three possible disagreement types:

1. **Consistency problem:** An existing rule was sufficient, but the reviewer applied it incorrectly.
2. **Definition gap:** The taxonomy did not adequately address the case.
3. **Defensible ambiguity:** Multiple interpretations were possible, and the reviewer's interpretation could be supported by the written rules.

No cases fell into these categories in the completed comparison.

### Was the Set Easy, or Were the Rules Clear?

The posts were generally understandable because the taxonomy provided explicit definitions and decision rules.

However, several examples required careful interpretation, especially posts containing numerical details that did not necessarily constitute an argument.

The 100% agreement suggests that the written rules were sufficiently clear for this particular set and that I applied them consistently with the staff labels.

It does not prove that the taxonomy would produce the same agreement rate on a larger or more difficult collection.

### Relationship to the GRC Classifier

The staff exercise was separate from the GRC classification dataset.

The staff labels were:

* `analysis`
* `hot_take`
* `reaction`

The GRC labels were:

* `ai_governance_policy`
* `ai_security_risk`
* `compliance_implementation`
* `vendor_third_party_risk`

Therefore, the 30 staff-labeled posts were **not added to the GRC training dataset**.

The GRC dataset remains at 20 labeled examples.

The staff exercise provides evidence of consistent application of an externally supplied taxonomy, but further independent review would be needed to establish agreement on the GRC taxonomy.

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

| # | Criterion                | Target                                | After Verdict                    |
| - | ------------------------ | ------------------------------------- | -------------------------------- |
| 1 | Held-out accuracy        | At least 72.5% across seeds           | **MISSED**                       |
| 2 | Per-label F1             | At least 0.50 across labels and seeds | **MISSED**                       |
| 3 | Maximum class proportion | No class above 40%                    | **MET**                          |
| 4 | Reviewer agreement       | At least 90%                          | **MET ON STAFF EXERCISE (100%)** |
| 5 | High-confidence accuracy | At least 80% above 77.5% confidence   | **NOT ESTABLISHED**              |

No original acceptance threshold was changed.

---

## What's Still Broken

### 1. Dataset Size

The project currently contains 20 labeled GRC examples rather than the required minimum of 150.

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

### 5. GRC-Specific Reviewer Agreement Not Tested

The separate staff-labeling exercise achieved 100% agreement, but the GRC dataset has not undergone an equivalent independent review.

**Next step:** Ask an independent reviewer to label a sample of GRC posts and compare their labels against the project annotations.

### 6. High-Confidence Threshold Not Evaluated

The saved evaluation contains summary confidence statistics but does not establish accuracy for predictions exceeding the original 77.5% threshold.

**Next step:** Save individual prediction probabilities and calculate confidence-filtered accuracy.

### 7. Evaluation Reliability

Each seed currently evaluates only three held-out examples.

**Next step:** Increase test-set size and use class-representative splits where feasible.

### The Gap Between Intended Labels and Learned Behavior

The taxonomy is designed to distinguish four different types of GRC discussions.

However, the model has not demonstrated reliable recognition of all four categories.

The available results suggest that the model is learning some governance-related patterns while failing to generalize consistently across the remaining categories.

The completed staff agreement exercise supports the ability to apply a written taxonomy consistently, but it does not establish that the project's GRC taxonomy is free of ambiguity.

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
10. Interpreting the staff taxonomy and reviewing staff-labeling examples.
11. Structuring the confusion matrix and error diagnosis.
12. Preparing the final project documentation.

The reported evaluation numbers come from executed experiments and the saved agreement report rather than AI-generated estimates.

Uncompleted measurements are identified explicitly instead of being presented as completed work.

---

## Reproducibility

### Project Files

| File                              | Purpose                                               |
| --------------------------------- | ----------------------------------------------------- |
| `takemeter.ipynb`                 | Training and evaluation notebook                      |
| `labels.csv`                      | Manually labeled GRC discussions                      |
| `label_definitions.txt`           | GRC label descriptions                                |
| `criteria.md`                     | Original acceptance criteria                          |
| `baseline.py`                     | Zero-shot baseline evaluation                         |
| `baseline_results.json`           | Baseline evaluation results                           |
| `results.json`                    | Initial trained-model evaluation and confusion matrix |
| `test_split.csv`                  | Saved initial test split                              |
| `results_three_seeds_before.json` | Three-seed evaluation with 3 epochs                   |
| `results_three_seeds_after.json`  | Three-seed evaluation with 5 epochs                   |
| `data/staff_posts.csv`            | Staff evaluation posts                                |
| `data/staff_taxonomy.md`          | Staff taxonomy and decision rules                     |
| `my_staff_labels.csv`             | My labels for the 30 staff posts                      |
| `agreement.py`                    | Staff agreement evaluation script                     |
| `agreement_results.json`          | Verified staff agreement results                      |
| `RUNNING.md`                      | Setup and execution instructions                      |

The official staff reference file, `data/staff_labels.csv`, is obtained from the course staff after independently completing the staff labels.

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

To reproduce the staff agreement exercise, first prepare `my_staff_labels.csv` using the staff taxonomy and obtain the official staff reference labels.

Then run:

```bash
python agreement.py
```

The notebook and scripts save evaluation results as JSON files for later comparison.

---

## Final Conclusion

This project investigated whether a fine-tuned DistilBERT model could classify information security community discussions into four AI and Technology GRC categories.

The initial three-seed experiment achieved:

* **Mean accuracy:** 33.3%.
* **Mean macro F1:** 0.217.

The five-epoch improvement experiment produced identical held-out metrics.

The zero-shot baseline achieved 0% accuracy on the three-example seed 42 test split, compared with 66.7% for the fine-tuned model.

The confusion matrix identified one vendor-risk discussion incorrectly classified as governance.

The separate staff taxonomy exercise achieved:

* **30 agreements out of 30 posts.**
* **100% agreement.**
* **Zero disagreements requiring adjudication.**

This completed the staff agreement exercise successfully. However, it does not establish agreement on the project's separate GRC taxonomy.

The original GRC classifier still does not satisfy the accuracy or per-label F1 acceptance criteria.

The confidence-filtered accuracy criterion also remains unverified.

The most important limitations are the small labeled GRC dataset, uneven category representation, and very small test splits.

**The main finding is that additional training epochs did not improve performance under the current data conditions.**

The project also demonstrated successful application of a separate, written staff taxonomy with complete agreement on the supplied evaluation set.

Future development should prioritize expanding the GRC dataset to at least 150 labeled examples, improving class coverage, obtaining independent GRC label reviews, and evaluating on larger test sets before considering the classifier reliable for practical GRC applications.

---

**Project repository:** https://github.com/ainny210/ai201-project3-takemeter-starter-v2026

**Setup instructions:** [RUNNING.md](RUNNING.md)
