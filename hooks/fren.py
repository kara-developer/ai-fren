#!/usr/bin/env python3
"""Claude Code PreToolUse freni.
Dışarıya bir şey gönderen komutta durur ve senden onay ister (ask).
Hiç yapılmaması gerekenleri tamamen engeller (deny).
Kendi araçlarına göre SOR ve YASAK listelerini düzenle."""
import json
import re
import sys

# Dışarı gönderen komutlar → önce sana sorar
SOR = [
    (r"api\.telegram\.org/bot[^\s'\"]*/send", "Telegram mesajı"),
    (r"\bsendmail\b|\bmail\s+-s\b|smtp", "e-posta gönderimi"),
    (r"graph\.facebook\.com/\S*/(messages|media_publish)", "Instagram/WhatsApp gönderimi"),
    (r"api\.twilio\.com", "SMS/WhatsApp gönderimi"),
    (r"\bgit\s+push\b", "koda canlı gönderim (git push)"),
]
# Asla yapılmayacaklar → tamamen engeller
YASAK = [
    (r"\brm\s+-rf\s+(/|~)(\s|$)", "ana klasörü silme"),
    (r"profile_picture|updateProfilePicture", "profil fotoğrafını değiştirme"),
]


def karar(dec, neden):
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse",
                                             "permissionDecision": dec,
                                             "permissionDecisionReason": neden}}, ensure_ascii=False))
    sys.exit(0)


def main():
    try:
        d = json.load(sys.stdin)
    except Exception:
        return
    if d.get("tool_name") != "Bash":
        return
    cmd = (d.get("tool_input") or {}).get("command", "")
    for pat, neden in YASAK:
        if re.search(pat, cmd):
            karar("deny", f"⛔ Yasak: {neden}.")
    for pat, ne in SOR:
        if re.search(pat, cmd):
            karar("ask", f"⚡ Dış aksiyon: {ne}. Kime, ne gidecek? Onaylıyor musun?")


if __name__ == "__main__":
    main()
