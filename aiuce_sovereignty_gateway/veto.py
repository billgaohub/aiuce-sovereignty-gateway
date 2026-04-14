"""
SovereigntyVeto dataclass — veto result container.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any, Optional


@dataclass
class SovereigntyVeto:
    """
    Represents a sovereignty veto decision returned by SovereigntyGateway.audit().

    Attributes:
        vetoed: Whether the intent was blocked.
        principle: The principle that triggered (e.g. P1_SOVEREIGNTY_SUPREME, DR1_DECISION_CONSERVATION).
        matched_pattern: The regex pattern that matched (P1-P7 only).
        reason: Human-readable explanation of the veto.
        severity: error | warning | info.
    """
    vetoed: bool
    principle: str
    matched_pattern: Optional[str] = None
    reason: str = ""
    severity: str = "error"  # error | warning | info

    def to_dict(self) -> Dict[str, Any]:
        """Serialize the veto to a dict with an ISO timestamp."""
        return {
            "vetoed": self.vetoed,
            "principle": self.principle,
            "matched_pattern": self.matched_pattern,
            "reason": self.reason,
            "severity": self.severity,
            "timestamp": datetime.now().isoformat(),
        }
