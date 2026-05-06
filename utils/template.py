"""utils/template.py — Build personalized email subject and body"""

import collections


DEFAULT_SUBJECT = (
    "Exploring {role} Opportunities at {company} — {sender_name}"
)

DEFAULT_BODY = """\
Hi {hr_name},

I hope you're doing well!

I came across {company} and was genuinely excited by the impact your team is making. \
I'm currently exploring {role} opportunities and believe my background could be a strong \
fit for what you're building.

A bit about me:
{highlights}

I'd love the chance to connect, learn more about your team, and explore whether there's \
a mutual fit. I've attached my resume for your reference.

You can reach me at:
  Email    : {sender_email}
  Phone    : {sender_phone}
  LinkedIn : {sender_linkedin}
  GitHub   : {sender_github}

Thank you for your time, {hr_name}. I look forward to hearing from you!

Warm regards,
{sender_name}
{sender_role}
"""


def _fill(template: str, placeholders: dict) -> str:
    """
    Fill template placeholders safely.
    Missing keys are left as empty strings instead of raising KeyError.
    """
    safe = collections.defaultdict(str, placeholders)
    return template.format_map(safe)


def _format_highlights(items: list) -> str:
    if not items:
        return "  • [Add your key achievements in config.json]"
    return "\n".join(f"  • {item}" for item in items)


def build_subject(config: dict, contact: dict) -> str:
    template = config.get("subject_template") or DEFAULT_SUBJECT
    return _fill(template, _placeholders(config, contact))


def build_body(config: dict, contact: dict) -> str:
    template = config.get("body_template") or DEFAULT_BODY
    return _fill(template, _placeholders(config, contact))


def _placeholders(config: dict, contact: dict) -> dict:
    return {
        "hr_name":         contact.get("name", "there"),
        "company":         contact.get("company", "your company"),
        "role":            contact.get("role", "the open position"),
        "sender_name":     config.get("sender_name", ""),
        "sender_role":     config.get("sender_role", ""),
        "sender_email":    config.get("sender_email", ""),
        "sender_phone":    config.get("sender_phone", "N/A"),
        "sender_linkedin": config.get("sender_linkedin", "N/A"),
        "sender_github":   config.get("sender_github", "N/A"),
        "highlights":      _format_highlights(config.get("highlights", [])),
    }
