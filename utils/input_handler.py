"""utils/input_handler.py — Collect HR contact details interactively"""


def _prompt(label: str, required: bool = True, default: str = "") -> str:
    suffix = f" [{default}]" if default else (" *" if required else " (optional)")
    while True:
        val = input(f"    {label}{suffix}: ").strip()
        if not val and default:
            return default
        if not val and required:
            print("      This field is required.")
            continue
        return val


def collect_hr_contacts(max_contacts: int = 5) -> list:
    print(f"\n  Enter up to {max_contacts} HR contacts.\n"
          "  Press Enter on 'HR Email' to stop early.\n")

    contacts = []

    for i in range(1, max_contacts + 1):
        print(f"  ── Contact {i} of {max_contacts} " + "─" * 30)

        email = input("    HR Email * (leave blank to finish): ").strip()
        if not email:
            break

        name    = _prompt("HR Name",                  required=False, default="there")
        company = _prompt("Company Name")
        role    = _prompt("Role you're applying for")

        contacts.append({
            "email":   email,
            "name":    name,
            "company": company,
            "role":    role,
        })

        print()

    return contacts


def confirm_send() -> bool:
    print()
    ans = input("  Send emails to all the above contacts? (yes/no): ").strip().lower()
    return ans == "yes"
