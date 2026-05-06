"""utils/display.py — CLI formatting and display helpers"""

VERSION = "1.0.0"


def print_banner():
    print()
    print("  ╔══════════════════════════════════════════════════════╗")
    print("  ║         Cold Email Bot  —  HR Outreach Tool          ║")
    print(f"  ║                     v{VERSION}                           ║")
    print("  ╚══════════════════════════════════════════════════════╝")
    print()


def print_summary_table(contacts: list[dict]):
    print("  ── Contacts to email " + "─" * 36)
    col = "  {:<3} {:<28} {:<22} {:<20}"
    print(col.format("#", "Email", "Company", "Role"))
    print("  " + "─" * 75)
    for i, c in enumerate(contacts, 1):
        print(col.format(
            i,
            c["email"][:26],
            c["company"][:20],
            c["role"][:18],
        ))
    print()


def print_result(index: int, contact: dict, status: str, note: str):
    icon  = "✓" if status == "SENT" else "✗"
    label = f"[{icon}] {status}"
    line  = f"  {index}. {label:<12} → {contact['email']}  ({contact['company']})"
    if note:
        line += f"\n       Error: {note}"
    print(line)
