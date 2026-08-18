"""Reusable reliability-aware risk policy for maintenance predictions."""

from dataclasses import asdict, dataclass
from typing import Literal

RiskLevel = Literal["LOW", "REVIEW", "HIGH"]
SupportState = Literal["SUPPORTED", "EDGE_CASE", "OUT_OF_DISTRIBUTION"]

LOW_TO_REVIEW = 0.04
REVIEW_TO_HIGH = 0.641


@dataclass(frozen=True)
class RiskDecision:
    probability: float
    model_risk: RiskLevel
    final_risk: RiskLevel
    input_support: SupportState
    human_review_required: bool
    reason: str

    def to_dict(self) -> dict:
        return asdict(self)


def assign_model_risk(probability: float) -> RiskLevel:
    """Map a calibrated failure probability to the frozen benchmark bands."""
    if not 0.0 <= probability <= 1.0:
        raise ValueError("probability must be between 0 and 1")
    if probability < LOW_TO_REVIEW:
        return "LOW"
    if probability < REVIEW_TO_HIGH:
        return "REVIEW"
    return "HIGH"


def reliability_aware_decision(
    probability: float,
    input_support: SupportState = "SUPPORTED",
    operating_context_supported: bool = True,
) -> RiskDecision:
    """Apply monotonic downgrades when evidence or context is unsupported."""
    model_risk = assign_model_risk(probability)

    if input_support == "OUT_OF_DISTRIBUTION":
        return RiskDecision(
            probability,
            model_risk,
            "REVIEW",
            input_support,
            True,
            "Input is outside validated support; prediction requires engineering review.",
        )

    if input_support == "EDGE_CASE" or not operating_context_supported:
        final_risk: RiskLevel = "REVIEW" if model_risk == "HIGH" else model_risk
        return RiskDecision(
            probability,
            model_risk,
            final_risk,
            input_support,
            True,
            "Evidence or operating context is limited; confidence was downgraded.",
        )

    return RiskDecision(
        probability,
        model_risk,
        model_risk,
        input_support,
        model_risk == "REVIEW",
        "Prediction is within validated input and operating support.",
    )


if __name__ == "__main__":
    example = reliability_aware_decision(
        probability=0.78,
        input_support="EDGE_CASE",
        operating_context_supported=True,
    )
    print(example.to_dict())
