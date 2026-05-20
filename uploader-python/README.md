# Python Uploader

This directory keeps a Python-focused copy of the existing upload and panel service files.

## Files

| File | Purpose |
| --- | --- |
| `server.py` | Python HTTP service and API entry |
| `config.py` | Paths, platform mapping, and network settings |
| `notification_scraper.py` | Platform notification scraping |
| `requirements.txt` | Python dependencies |
| `start.bat` / `start.sh` | Windows and Unix startup scripts |

## External Dependency

The actual platform upload capability can be provided by `social-auto-upload`.

Configure its location with:

```bash
SAU_ROOT=/path/to/social-auto-upload
```

## Usage

```bash
pip install -r requirements.txt
python server.py
```

## Notes

- Keep the existing upload behavior stable.
- Avoid rewriting `social-auto-upload` logic inside this repository.
- The project root still contains the runnable Python prototype.
