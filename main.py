import os
import sys
from utils.input_handler import collect_hr_contacts, confirm_send
from utils.email_sender  import EmailSender
from utils.tracker       import Tracker
from utils.display       import print_banner, print_summary_table, print_result
from utils.config_loader import load_config


def main():
    print_banner()

    config = load_config("config.json")
 
    resume_path = config.get("resume_path", "resume/resume.pdf")
    if not os.path.exists(resume_path):
        print(f"\n  [!] Resume not found at: {resume_path}")
        print("      Place your PDF resume there and try again.\n")
        sys.exit(1)

    # Collect HR contacts interactively 
    contacts = collect_hr_contacts(max_contacts=5)
    if not contacts:
        print("\n  No contacts entered. Exiting.\n")
        sys.exit(0)

    print_summary_table(contacts)

    # Pre-send duplicate check against tracker 
    tracker = Tracker("logs/tracker.json")
    already_contacted = tracker.find_duplicates(contacts)
    if already_contacted:
        print("  ⚠  The following contacts were already emailed previously:")
        for entry in already_contacted:
            print(f"     • {entry['hr_email']}  ({entry['company']})  — {entry['timestamp']}")
        print()
        ans = input("  Continue anyway? (yes/no): ").strip().lower()
        if ans != "yes":
            print("\n  Cancelled. No emails were sent.\n")
            sys.exit(0)
        print()

    if not confirm_send():
        print("\n  Cancelled. No emails were sent.\n")
        sys.exit(0)

    print("\n  Sending emails...\n")

    with EmailSender(config) as sender:
        for i, contact in enumerate(contacts, 1):
            status, note = sender.send(contact, resume_path)
            tracker.update(contact, status, note)
            print_result(i, contact, status, note)

    tracker.save()
    print("\n" + "─" * 58)
    print("  All done! Tracker updated → logs/tracker.json")
    print("─" * 58 + "\n")
    tracker.print_report()


if __name__ == "__main__":
    main()
