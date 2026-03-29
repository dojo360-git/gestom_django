import json
import os
from pathlib import Path

import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv


env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path)

DB_NAME = os.getenv("DB_NAME", "bdd_regie")
DB_USER = os.getenv("DB_USER", "super_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")


SQL = """
SELECT
    v.id_collecte,
    v.id_agent,
    v.date_collecte AS date,
    CASE
        WHEN v.hr_debut IS NOT NULL AND v.hr_fin IS NOT NULL THEN
            EXTRACT(
                EPOCH FROM (
                    CASE
                        WHEN v.hr_fin >= v.hr_debut THEN (v.hr_fin - v.hr_debut)
                        ELSE (v.hr_fin - v.hr_debut + interval '24 hours')
                    END
                )
            )::bigint
        ELSE 0
    END AS duree_sec
FROM core_collecte c
CROSS JOIN LATERAL (
    VALUES
        (c.id_collecte, c.id_agent_1_id, c.date_collecte, c.a1_hr_debut, c.a1_hr_fin),
        (c.id_collecte, c.id_agent_2_id, c.date_collecte, c.a2_hr_debut, c.a2_hr_fin),
        (c.id_collecte, c.id_agent_3_id, c.date_collecte, c.a3_hr_debut, c.a3_hr_fin)
) AS v(id_collecte, id_agent, date_collecte, hr_debut, hr_fin)
WHERE v.id_agent IS NOT NULL
ORDER BY v.date_collecte, v.id_collecte, v.id_agent;
"""


def main():
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=int(DB_PORT),
    )

    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(SQL)
            rows = cursor.fetchall()

        print(json.dumps(rows, indent=2, ensure_ascii=False, default=str))
    finally:
        conn.close()


if __name__ == "__main__":
    main()
