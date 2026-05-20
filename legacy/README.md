# Legacy Python Prototype

This directory documents the original runnable prototype that still lives at the project root.

## Root Files

| File | Purpose |
| --- | --- |
| `index.html` | Single-page panel UI |
| `server.py` | Python HTTP service |
| `config.py` | Python configuration |
| `notification_scraper.py` | Notification scraping |
| `requirements.txt` | Python dependencies |
| `start.bat` | Windows startup script |
| `start.sh` | Unix startup script |

## Run

```bash
pip install -r requirements.txt
python server.py
```

Then open:

```text
http://127.0.0.1:8787
```

## Status

- The legacy Python prototype remains the current runnable product baseline.
- New Web/Desktop shells can migrate this UI gradually.
- The Python files have also been copied to `uploader-python/` for later modularization.
