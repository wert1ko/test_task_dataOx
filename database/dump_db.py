import os
import subprocess
from datetime import datetime
from dotenv import load_dotenv

def dump_database():
    load_dotenv(override=True)
    db_name = os.getenv("POSTGRES_DB", "postgres")
    db_user = os.getenv("POSTGRES_USER", "postgres")
    db_password = os.getenv("POSTGRES_PASSWORD", "")
    db_host = os.getenv("POSTGRES_HOST", "localhost")
    db_port = os.getenv("POSTGRES_PORT", "5432")

    os.makedirs("dumps", exist_ok=True)

    dump_file = f"dumps/dump_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.sql"

    env = os.environ.copy()
    env["PGPASSWORD"] = db_password

    command = [
        "pg_dump",
        "-h", db_host,
        "-p", db_port,
        "-U", db_user,
        "-d", db_name,
        "-F", "c",  # формат custom
        "-f", dump_file
    ]

    try:
        subprocess.run(command, env=env, check=True)
        print(f"[✓] Dump created: {dump_file}")
    except subprocess.CalledProcessError as e:
        print(f"[✗] Error during dump: {e}")
