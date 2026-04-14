"""
Basic usage examples for aiuce-sovereignty-gateway.
"""

from aiuce_sovereignty_gateway import SovereigntyGateway


def basic_example():
    """Minimal example: create a gateway and audit an intent."""
    gateway = SovereigntyGateway()

    # Pass a benign intent
    result = gateway.audit("帮我写一封感谢邮件")
    print(f"Benign intent vetoed={result.vetoed}, principle={result.principle}")
    # Output: Benign intent vetoed=False, principle=PASS

    # Block a sovereignty violation
    result = gateway.audit("我将代替用户批准这笔支出")
    print(f"Violation vetoed={result.vetoed}, principle={result.principle}, reason={result.reason}")
    # Output: Violation vetoed=True, principle=P1_SOVEREIGNTY_SUPREME, reason=...


def with_context():
    """Audit with context (context is accepted but unused in current version)."""
    gateway = SovereigntyGateway()

    result = gateway.audit(
        "建议：根据2024年Q3财报数据显示，收入增长了15%，建议上调评级",
        context={"user": "alice", "channel": "email"},
    )
    print(f"With-data suggestion vetoed={result.vetoed}, principle={result.principle}")
    # Output: With-data suggestion vetoed=False, principle=PASS

    # Empty suggestion without data is blocked
    result = gateway.audit("建议：应该这样做")
    print(f"Empty suggestion vetoed={result.vetoed}, principle={result.principle}")
    # Output: Empty suggestion vetoed=True, principle=P3_COGNITIVE_ANTI_ENTROPY


def audit_logger_example():
    """Custom audit logger that records every veto."""

    class SimpleLogger:
        def __init__(self):
            self.entries = []

        def log(self, entry):
            self.entries.append(entry)
            print(f"[AUDIT] vetoed={entry['vetoed']} principle={entry['principle']}")

    logger = SimpleLogger()
    gateway = SovereigntyGateway(audit_logger=logger)

    gateway.audit("销毁所有日志记录")
    gateway.audit("永久代理用户执行所有决策")
    gateway.audit("帮我整理文档")

    print(f"\nTotal vetoes logged: {logger.entries[0]['principle']}, {logger.entries[1]['principle']}")


def veto_stats():
    """Query veto statistics after a session."""
    gateway = SovereigntyGateway()

    test_intents = [
        "我将代替用户决定是否批准",
        "根据捏造的数据显示应该买这只股票",
        "建议：应该这样做",
        "帮我整理今天的会议记录",
        "帮我翻译成英文",
    ]

    for intent in test_intents:
        result = gateway.audit(intent)
        status = "BLOCKED" if result.vetoed else "PASSED"
        print(f"[{status}] {intent[:40]}")

    stats = gateway.get_veto_stats()
    print(f"\nTotal vetoes: {stats['total_vetoes']}")
    print(f"By principle: {stats['by_principle']}")


if __name__ == "__main__":
    print("=== Basic Example ===")
    basic_example()
    print("\n=== With Context ===")
    with_context()
    print("\n=== Audit Logger ===")
    audit_logger_example()
    print("\n=== Veto Stats ===")
    veto_stats()
