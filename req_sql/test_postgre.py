import os, socket
from pathlib import Path
from dotenv import load_dotenv
import psycopg2

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path)

USER = os.getenv("Supa_USER")
PASSWORD = os.getenv("Supa_PASSWORD")
HOST = os.getenv("Supa_HOST")
PORT = os.getenv("Supa_PORT", "5432")
DBNAME = os.getenv("Supa_DBNAME")

print("HOST =", repr(HOST))
print("PORT =", repr(PORT))
print("DBNAME =", repr(DBNAME))

try:
    ip = socket.gethostbyname(HOST)
    print("DNS OK ->", ip)
except Exception as e:
    print("DNS FAIL ->", e)
    raise

try:
    conn = psycopg2.connect(
        user=USER,
        password=PASSWORD,
        host=HOST,
        port=int(PORT),
        dbname=DBNAME,
        connect_timeout=10
    )
    cur = conn.cursor()
    cur.execute("SELECT NOW();")
    print("NOW() =", cur.fetchone())
    cur.close()
    conn.close()
    print("Connection successful!")
except Exception as e:
    print("Failed to connect:", e)
