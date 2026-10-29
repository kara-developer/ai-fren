# Yapay zekana fren tak

Yapay zekan e-posta atabiliyor, mesaj yazabiliyor, gönderi planlayabiliyorsa bir gün senden habersiz bir şey göndermesi an meselesi. Bu paket araya bir **fren** koyar: dışarıya bir şey gidecekse yapay zeka durur, kime ne gideceğini gösterir, sen onaylamadan çıkmaz.

**Neden talimat değil kod?** "Onaysız mesaj atma" diye yazmak yetmez; uzun bir işte talimat unutulabilir. Kod unutmaz: her komuttan önce çalışır.

## Nasıl çalışır (Claude Code)
Claude Code'da her komuttan önce çalışan küçük betiklere **hook** denir. `hooks/fren.py`:
- **SOR listesi:** dışarı gönderen komut (Telegram, e-posta, Instagram, SMS, git push…) → Claude durur ve sana sorar.
- **YASAK listesi:** asla yapılmayacaklar (ör. profil fotoğrafını değiştirmek) → tamamen engellenir.

## Kurulum (2 dakika)
1. `hooks/fren.py` dosyasını `~/.claude/hooks/` içine kopyala.
2. `~/.claude/settings.json` dosyasına ekle:
```json
{
  "hooks": {
    "PreToolUse": [
      { "matcher": "Bash", "hooks": [ { "type": "command", "command": "python3 ~/.claude/hooks/fren.py" } ] }
    ]
  }
}
```
3. Dene: Claude'a "şu adrese test e-postası at" de → onay sorusu gelmeli.
4. Listeleri kendi araçlarına göre düzenle (kendin yapamazsan `PROMPT.md`'yi Claude'a ver).

## Dikkat
- Fren yalnızca listedeki kalıpları yakalar; yeni bir gönderim aracı eklediğinde listeye de ekle.
- ChatGPT/Gemini gibi sohbet uygulamalarında hook yok; orada bilgisayarına erişim veren araçları kullanmadan önce benzer onay ayarlarına bak.
