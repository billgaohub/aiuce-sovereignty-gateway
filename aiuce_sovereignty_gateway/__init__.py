"""
AIUCE Sovereignty Gateway.

The deterministic constitutional layer for AI agents.  Zero LLM calls; every
check is a provable boolean regex match or function evaluation.

Exports:
    SovereigntyGateway
    SovereigntyPrinciples
    SovereigntyVeto
    DecisionRightsPrinciples
"""

from .gateway import SovereigntyGateway
from .principles import SovereigntyPrinciples, DecisionRightsPrinciples
from .veto import SovereigntyVeto

__all__ = [
    "SovereigntyGateway",
    "SovereigntyPrinciples",
    "SovereigntyVeto",
    "DecisionRightsPrinciples",
]

__version__ = "0.1.0"
