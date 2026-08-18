# Model Card

## Intended use

Prioritize equipment inspections and support maintenance planning by combining failure-risk prediction with calibrated confidence, explanation, input-support checks, and human escalation.

The system is decision support. It does not establish physical root cause, replace qualified maintenance personnel, or authorize autonomous shutdown or repair.

## Benchmark dataset and split

The reported binary failure-risk metrics use a held-out evaluation set of 1,500 observations. Because equipment failures are rare, model selection emphasized precision-recall performance and false-negative analysis rather than accuracy alone.

## Candidate models

- Logistic Regression
- Random Forest
- Gradient Boosting
- Extra Trees
- XGBoost

Randomized hyperparameter search and cross-validation were used for the leading Random Forest and XGBoost candidates. Sigmoid calibration was then evaluated on the selected pipelines.

## Final benchmark comparison

| Metric | Calibrated Random Forest | Calibrated XGBoost |
|---|---:|---:|
| Precision | 0.8936 | 0.8400 |
| Recall | 0.8235 | 0.8235 |
| F1 | 0.8571 | 0.8317 |
| ROC-AUC | 0.9835 | 0.9858 |
| PR-AUC | 0.9039 | 0.8760 |
| Brier score | 0.0085 | 0.0099 |
| Log loss | 0.0366 | 0.0431 |

The calibrated Random Forest was selected because it achieved better precision, F1, PR-AUC, Brier score, and log loss at the same recall.

## Risk policy

- `LOW`: probability below `0.04`
- `REVIEW`: probability from `0.04` to below `0.641`
- `HIGH`: probability at or above `0.641`

The thresholds are frozen evaluation policies, not universal industrial safety limits. Deployment to a new asset class requires validation against its failure costs, sensor behavior, operating regimes, and maintenance procedures.

## Explainability

The leading global drivers in the benchmark evaluation included:

| Feature | Mean importance |
|---|---:|
| Temperature difference | 0.4350 |
| Mechanical power proxy | 0.1340 |
| Wear x Torque | 0.1248 |

Local explanations are intended to show which observed signals influenced the prediction. They should not be interpreted as causal root-cause proof.

## Reliability safeguards

- calibrated probabilities;
- range-based and latent-space input support checks;
- operating-regime and stability policies;
- explicit limitations in every response;
- automatic reliability downgrade for unsupported evidence;
- mandatory human review for uncertain or conflicting cases.

## Known limitations

- benchmark metrics do not guarantee field performance on a different machine population;
- rare failures make threshold choice sensitive to the cost of missed events and unnecessary inspections;
- maintenance records and manuals can be incomplete or outdated;
- sensor drift, repairs, load changes, and unseen fault modes can invalidate learned relationships;
- explanation methods describe model behavior, not physical causality.
