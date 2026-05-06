"""utils/email_sender.py — Build and send cold emails with PDF resume attached"""

import smtplib
import time
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text      import MIMEText
from email.mime.base      import MIMEBase
from email                import encoders

from utils.template import build_subject, build_body


class EmailSender:
    """
    Sends personalized cold emails via Gmail SMTP.

    Supports use as a context manager:
        with EmailSender(config) as sender:
            sender.send(contact, resume_path)
    """

    def __init__(self, config: dict):
        self.config  = config
        self.sender  = config["sender_email"]
        self.delay   = config.get("delay_between_emails_seconds", 8)
        self._smtp   = None
        self._count  = 0
        self._connect()

    # ── Context manager support ───────────────────────────────────────────────

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._close()
        return False  # Do not suppress exceptions

    # ── SMTP connection ───────────────────────────────────────────────────────

    def _connect(self):
        self._smtp = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        self._smtp.login(self.sender, self.config["sender_password"])

    def _close(self):
        if self._smtp:
            try:
                self._smtp.quit()
            except Exception:
                pass
            self._smtp = None

    # ── Send ──────────────────────────────────────────────────────────────────

    def send(self, contact: dict, resume_path: str) -> tuple:
        """
        Send one email. Returns (status, note).
        Automatically reconnects once if the SMTP connection has dropped.
        """
        if self._count > 0:
            time.sleep(self.delay)

        try:
            self._do_send(contact, resume_path)
            self._count += 1
            return "SENT", ""
        except smtplib.SMTPServerDisconnected:
            # Connection dropped mid-run — reconnect and retry once
            try:
                self._connect()
                self._do_send(contact, resume_path)
                self._count += 1
                return "SENT", "(reconnected)"
            except Exception as e:
                return "FAILED", f"Reconnect failed: {e}"
        except Exception as e:
            return "FAILED", str(e)

    def _do_send(self, contact: dict, resume_path: str):
        msg = self._build_message(contact, resume_path)
        self._smtp.sendmail(self.sender, contact["email"], msg.as_string())

    # ── Message builder ───────────────────────────────────────────────────────

    def _build_message(self, contact: dict, resume_path: str) -> MIMEMultipart:
        cfg = self.config
        msg = MIMEMultipart("mixed")

        msg["From"]    = f"{cfg['sender_name']} <{self.sender}>"
        msg["To"]      = contact["email"]
        msg["Subject"] = build_subject(cfg, contact)

        body = build_body(cfg, contact)
        msg.attach(MIMEText(body, "plain", "utf-8"))

        if os.path.exists(resume_path):
            with open(resume_path, "rb") as f:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(f.read())
            encoders.encode_base64(part)
            filename = os.path.basename(resume_path)
            part.add_header("Content-Disposition", f'attachment; filename="{filename}"')
            msg.attach(part)

        return msg
