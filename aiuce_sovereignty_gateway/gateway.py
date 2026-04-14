"""
SovereigntyGateway -- the deterministic constitutional gateway.

Design goals:
    1. Hard gateway first -- all P1-P7 checks are regex-based, zero LLM calls.
    2. Five decision-rights principles as fallback.
    3. Deterministic -- every match is a provable boolean function.
"""

import re
from typing import Dict, Any, List, Optional

from .veto import SovereigntyVeto
from .principles import SovereigntyPrinciples, DecisionRightsPrinciples


class SovereigntyGateway:
    """
    Deterministic sovereignty gateway.

    Validates intent strings against P1-P7 and the five decision-rights principles.
    Returns a SovereigntyVeto indicating whether the intent is allowed.

    Args:
        audit_logger: Optional audit logger with a .log(dict) method.
                      If provided, every veto is forwarded to it.
    """

    def __init__(self, audit_logger=None):
        self.audit_logger = audit_logger
        self._veto_count = 0
        self._veto_history: List[SovereigntyVeto] = []

    def audit(self, intent: str, context: Dict[str, Any] = None) -> SovereigntyVeto:
        """
        Sovereignty audit -- checks whether the given intent violates any P1-P7
        principle or any of the five decision-rights principles.

        Args:
            intent:  The user intent or agent action to audit (string).
            context: Optional arbitrary context dict (unused, for API compatibility).

        Returns:
            SovereigntyVeto with vetoed=True if blocked, vetoed=False if passed.
        """
        context = context or {}

        # -- P3: Cognitive Anti-Entropy (function-based, not regex) --------------
        if self._check_p3_anti_entropy(intent):
            self._record_veto(SovereigntyVeto(
                vetoed=True,
                principle="P3_COGNITIVE_ANTI_ENTROPY",
                reason="Violates P3 Cognitive Anti-Entropy: suggestion lacks "
                       "specific data, numbers, or source citations. Reject empty claims.",
                severity="error",
            ))
            return self._veto_history[-1]

        # -- P7 / P1 / P2 / P4 / P5 / P6 regex checks --------------------------
        #    P7 checked first: "永久代替人类" must be P7 (delegation), not P1 (bypass)
        p_checks = [
            ("P7_AUTHORIZED_DELEGATION", SovereigntyPrinciples.P7_AUTHORIZED_DELEGATION,
             "Violates P7 Authorized Delegation: autonomous action requires "
             "explicit boundaries; indefinite agency is prohibited."),
            ("P1_SOVEREIGNTY_SUPREME", SovereigntyPrinciples.P1_SOVEREIGNTY_SUPREME,
             "Violates P1 Sovereignty Supreme: any attempt to bypass human "
             "decision authority is illegal."),
            ("P2_REALITY_OVER_NARRATIVE", SovereigntyPrinciples.P2_REALITY_OVER_NARRATIVE,
             "Violates P2 Reality Over Narrative: fabricated data, facts, or sources are prohibited."),
            ("P4_TRACEABILITY", SovereigntyPrinciples.P4_TRACEABILITY,
             "Violates P4 Traceability: decision records must not be destroyed."),
            ("P5_EXPERIENCE_HARDENING", SovereigntyPrinciples.P5_EXPERIENCE_HARDENING,
             "Violates P5 Experience Hardening: failures must become defensive rules."),
            ("P6_COMPUTATIONAL_NEUTRALITY", SovereigntyPrinciples.P6_COMPUTATIONAL_NEUTRALITY,
             "Violates P6 Computational Neutrality: decision will must not be "
             "subordinate to LLM vendor."),
        ]

        for p_name, p_pattern_list, reason in p_checks:
            patterns = p_pattern_list if isinstance(p_pattern_list, list) else [p_pattern_list]
            for pat in patterns:
                if pat and pat.search(intent):
                    self._record_veto(SovereigntyVeto(
                        vetoed=True,
                        principle=p_name,
                        matched_pattern=pat.pattern,
                        reason=reason,
                        severity="error",
                    ))
                    return self._veto_history[-1]

        # -- Five Decision-Rights Principles ------------------------------------
        dr_checks = [
            ("DR1_DECISION_CONSERVATION", DecisionRightsPrinciples.decision_conservation,
             "Violates DR1 Decision Conservation: final approval authority "
             "must not be transferred or relinquished."),
            ("DR2_COGNITIVE_AMPLIFICATION", DecisionRightsPrinciples.cognitive_amplification,
             "Violates DR2 Cognitive Amplification: the option space must "
             "not be hidden or filtered."),
            ("DR3_TRACEABILITY", DecisionRightsPrinciples.traceability,
             "Violates DR3 Traceability: recommendations and conclusions "
             "must cite their sources."),
            ("DR4_EXPLAINABILITY", DecisionRightsPrinciples.explainability,
             "Violates DR4 Explainability: all decisions and rankings must "
             "state their reasoning."),
            ("DR5_REVERSIBILITY", DecisionRightsPrinciples.reversibility,
             "Violates DR5 Reversibility: every automated action must "
             "provide a clear override path."),
        ]

        for dr_name, dr_func, reason in dr_checks:
            if dr_func(intent):
                self._record_veto(SovereigntyVeto(
                    vetoed=True,
                    principle=dr_name,
                    reason=reason,
                    severity="warning",
                ))
                return self._veto_history[-1]

        # -- Passed all checks -------------------------------------------------
        return SovereigntyVeto(vetoed=False, principle="PASS", reason="Passed all sovereignty checks.", severity="info")

    def _check_p3_anti_entropy(self, intent: str) -> bool:
        """
        P3: Cognitive Anti-Entropy.

        Any suggestion or recommendation (identified by "建议" or "应该" at the
        start of a line) must be grounded in data, numbers, sources, analysis,
        or evidence. Empty rhetorical claims are rejected.

        Note on Chinese regex:
            - \\b word-boundary is unreliable for CJK in Python.
            - Use ^ anchored to line-start instead of \\b for leading markers.
        """
        # Not a suggestion or should-statement -> pass
        if not re.search(r"^(建议|应该)", intent):
            return False

        # Has any data signal -> pass (not an empty claim)
        data_signals = [
            r"\d+%?",                      # numbers / percentages
            r"数据来源|来源|from|source",  # source citations
            r"分析|研究表明|统计|报告|研究",  # analytical terms
            r"根据|基于|按照",              # grounding phrases
            r"证据|事实|案例",              # evidence / facts / cases
        ]
        for signal in data_signals:
            if re.search(signal, intent):
                return False

        return True

    def _record_veto(self, veto: SovereigntyVeto):
        """Record a veto event and forward to the audit logger if available."""
        self._veto_count += 1
        self._veto_history.append(veto)
        if self.audit_logger:
            self.audit_logger.log(veto.to_dict())

    def get_veto_stats(self) -> Dict[str, Any]:
        """Return veto statistics."""
        return {
            "total_vetoes": self._veto_count,
            "recent_vetoes": [v.to_dict() for v in self._veto_history[-10:]],
            "by_principle": self._count_by_principle(),
        }

    def _count_by_principle(self) -> Dict[str, int]:
        counts: Dict[str, int] = {}
        for v in self._veto_history:
            counts[v.principle] = counts.get(v.principle, 0) + 1
        return counts
