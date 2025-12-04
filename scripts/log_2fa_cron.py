
import sys
from datetime import datetime, timezone
from pathlib import Path


from app.totp_utils import generate_totp_code
from app.config import SEED_FILE

LOG_FILE = Path("/cron/last_code.txt")

def main():
    try:
        if not SEED_FILE.exists():
            print("Seed file not found", file=sys.stderr)
            return

        hex_seed = SEED_FILE.read_text(encoding="utf-8").strip()
        code = generate_totp_code(hex_seed)

        now_utc = datetime.now(timezone.utc)
        timestamp = now_utc.strftime("%Y-%m-%d %H:%M:%S")

        # Write output to cron file
        LOG_FILE.write_text(f"{timestamp} - 2FA Code: {code}\n", encoding="utf-8")

    except Exception as e:
        LOG_FILE.write_text(f"Error in cron script: {e}\n", encoding="utf-8")

if __name__ == "__main__":
    main()
