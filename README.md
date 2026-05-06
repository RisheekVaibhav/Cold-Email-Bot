# Cold Email Bot — HR Outreach Automation

A clean Python CLI tool to send personalized cold emails with your resume attached to multiple HR contacts — and track which companies you've already reached out to.

---

## Features

- **Interactive input** — enter up to 5 HR contacts per run (name, email, company, role)
- **Personalized emails** — each email auto-fills HR name, company, and the role you want
- **Resume attached** — your PDF resume is attached to every email automatically
- **Company tracker** — `logs/tracker.json` is updated after every send so you always know who you've contacted
- **Zero dependencies** — uses Python standard library only (no pip install needed)
- **Gmail SMTP** — works out of the box with a Gmail App Password

---

## Project Structure

```
cold-email-bot/
├── main.py                  # Entry point — run this
├── config.example.json      # Template for your config (safe to commit)
├── config.json              # Your real config — gitignored, never commit
├── requirements.txt
├── .gitignore
├── resume/
│   └── resume.pdf           # Place your resume here — gitignored
├── logs/
│   └── tracker.json         # Auto-generated; tracks every email sent
└── utils/
    ├── config_loader.py
    ├── display.py
    ├── email_sender.py
    ├── input_handler.py
    ├── template.py
    └── tracker.py
```

---

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/yourusername/cold-email-bot.git
cd cold-email-bot
```

**2. Create your config**
```bash
cp config.example.json config.json
```
Open `config.json` and fill in your name, Gmail address, App Password, LinkedIn, GitHub, and your 3–5 highlight bullet points.

**3. Get a Gmail App Password**

> You must use an **App Password**, not your regular Gmail password.

1. Go to [myaccount.google.com/security](https://myaccount.google.com/security)
2. Enable **2-Step Verification** if not already on
3. Search for **App Passwords**
4. Create one for "Mail" → copy the 16-character password into `config.json`

**4. Add your resume**
```bash
# Place your PDF resume in the resume/ folder
cp ~/Downloads/YourResume.pdf resume/resume.pdf
```

---

## Usage

```bash
python main.py
```

You'll be prompted to enter up to 5 HR contacts:

```
  ── Contact 1 of 5 ──────────────────────────────
    HR Email * (leave blank to finish): hr@google.com
    HR Name (optional) [there]: Priya Sharma
    Company Name *: Google
    Role you're applying for *: Software Engineer
```

After entering all contacts you'll see a summary table and a confirmation prompt before anything is sent.

---

## Tracker

Every send updates `logs/tracker.json`. Example:

```json
[
  {
    "timestamp": "2026-04-09 14:32:01",
    "company": "Google",
    "hr_name": "Priya Sharma",
    "hr_email": "hr@google.com",
    "role": "Software Engineer",
    "status": "SENT",
    "note": ""
  }
]
```

At the end of each run the tracker prints a report:

```
  Total companies contacted : 5
  Failed                    : 0

  Company                Role                 Status
  ────────────────────────────────────────────────────
  Google                 Software Engineer    SENT
  Microsoft              Backend Engineer     SENT
  ...
```

---

## Customizing the Email

The default body template is in `utils/template.py`. You can override it in `config.json`:

```json
"body_template": "Hi {hr_name},\n\n..."
```

Available placeholders:

| Placeholder | Source |
|---|---|
| `{hr_name}` | Entered at runtime |
| `{company}` | Entered at runtime |
| `{role}` | Entered at runtime |
| `{sender_name}` | config.json |
| `{sender_role}` | config.json |
| `{sender_email}` | config.json |
| `{sender_phone}` | config.json |
| `{sender_linkedin}` | config.json |
| `{sender_github}` | config.json |
| `{highlights}` | config.json (list → bullet points) |

---

## Security Notes

- `config.json` and `resume/` are in `.gitignore` — they will **never** be committed
- Only `config.example.json` (with placeholder values) is committed
- Do not hardcode credentials anywhere in source files

---

## Requirements

- Python 3.9+
- Gmail account with 2-Step Verification enabled
- A Gmail App Password

---

## License

MIT
