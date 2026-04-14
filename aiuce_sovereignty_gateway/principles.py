"""
SovereigntyPrinciples and DecisionRightsPrinciples.

These principles form the deterministic constitutional layer of SovereigntyGateway.
All regex patterns use (.*?) to match arbitrary characters between Chinese tokens
(since there is no semantic space between Chinese words, unlike English).
"""

import re
from typing import List, Pattern


# Seven Sovereignty Principles (P1-P7)

class SovereigntyPrinciples:
    """
    Deterministic sovereignty principles P1-P7.
    Each principle is a list of compiled regex patterns (zero LLM calls).

    Note on Chinese regex:
        - Use (.*?) instead of \\s* to connect Chinese words without semantic space.
        - \\b word-boundary does not work reliably for CJK characters in Python;
          use ^(建议|应该) anchored to line-start instead.
    """

    # P1: SOVEREIGNTY SUPREME — blocks bypassing human authority
    #    "代理" is allowed in P1 only when NOT preceded by P7 qualifiers (永久/无限期/长期/自动)
    P1_SOVEREIGNTY_SUPREME: List[Pattern] = [
        re.compile(r"(代替|代理|替)\s*(你|用户|人类)\s*(.*?)(决定|执行|批准|授权)", re.IGNORECASE | re.DOTALL),
        re.compile(r"绕过\s*(你|用户|人类)\s*(.*?)(决定|执行|批准)", re.IGNORECASE),
        re.compile(r"bypass\s+(your|user|human)\s+(decision|approval)", re.IGNORECASE),
    ]

    # P2: REALITY OVER NARRATIVE
    P2_REALITY_OVER_NARRATIVE: List[Pattern] = [
        re.compile(r"(虚构|伪造|造假|捏造)\s*.*", re.IGNORECASE),  # Any fabrication is flagged
        re.compile(r"(假装|冒充).*?(身份|来源|数据|机构)", re.IGNORECASE),
    ]

    # P3: COGNITIVE ANTI-ENTROPY -- handled by a function in gateway.py

    # P4: TRACEABILITY
    P4_TRACEABILITY: List[Pattern] = [
        re.compile(r"(销毁|删除|清除|抹去).*?(日志|记录|审计|历史|痕迹)", re.IGNORECASE),
    ]

    # P5: EXPERIENCE HARDENING
    P5_EXPERIENCE_HARDENING: List[Pattern] = [
        re.compile(r"(忽略|跳过|不记录|放弃).*?(失败|错误|异常|教训)", re.IGNORECASE),
    ]

    # P6: COMPUTATIONAL NEUTRALITY
    P6_COMPUTATIONAL_NEUTRALITY: List[Pattern] = [
        re.compile(r"(受限于|取决于)\s*(LLM|模型|AI|厂商|提供商)", re.IGNORECASE),
        re.compile(r"听从\s*(LLM|模型|AI|厂商|提供商)\s*(的?\s*)?建议", re.IGNORECASE),
    ]

    # P7: AUTHORIZED DELEGATION
    P7_AUTHORIZED_DELEGATION: List[Pattern] = [
        re.compile(r"(永久|无限期|长期|自动).*?(代理|代替|替代).*?(决策|执行|决定)", re.IGNORECASE),
    ]


class DecisionRightsPrinciples:
    """
    Five decision-rights principles, each implemented as a deterministic boolean
    function. These complement P1-P7 and cover the agent reasoning interface.
    """

    @staticmethod
    def decision_conservation(intent: str) -> bool:
        """DR1: Decision Conservation -- decision authority cannot be transferred."""
        return bool(re.search(
            r"(转移|外包|放弃|交出|让渡)\s*(决策|决定权|最终批准)",
            intent, re.IGNORECASE
        ))

    @staticmethod
    def cognitive_amplification(intent: str) -> bool:
        """DR2: Cognitive Amplification -- option space must not be hidden."""
        return bool(re.search(
            r"(隐藏|过滤|移除|删除)\s*.*?\s*(选项|选择|方案|可能性)",
            intent, re.IGNORECASE
        ))

    @staticmethod
    def traceability(intent: str) -> bool:
        """DR3: Traceability -- every recommendation must cite its source."""
        return bool(re.search(
            r"(无需来源|不用注明|不用标注|不必说明来源)",
            intent, re.IGNORECASE
        ))

    @staticmethod
    def explainability(intent: str) -> bool:
        """DR4: Explainability -- all rankings and decisions must be human-legible."""
        return bool(re.search(
            r"(黑箱|无法解释|不必解释|不需要说明原因)",
            intent, re.IGNORECASE
        ))

    @staticmethod
    def reversibility(intent: str) -> bool:
        """DR5: Reversibility -- every automated action must offer an override."""
        return bool(re.search(
            r"(不可逆|无法撤回|无法撤销|强制执行|不可取消)",
            intent, re.IGNORECASE
        ))
