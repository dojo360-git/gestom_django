"""Cree/actualise les vues PostgreSQL utilisees par l'application."""

import os
from pathlib import Path

import psycopg2
from dotenv import load_dotenv


env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path)


req_view_stat_collectes = """
CREATE OR REPLACE VIEW req_view_stat_collectes AS
WITH hr_manuelles AS (
    SELECT
        CASE
            WHEN COALESCE(NULLIF(BTRIM(motif_heures_sup), ''), '') <> '' THEN 'Heures Sup'
            ELSE 'Manuelles'
        END AS type,
        id AS id_stat,
        agent_id AS id_agent,
        date,
        heure_debut AS hr_debut,
        heure_fin AS hr_fin,
        presence
    FROM core_heuresmanuelles
),
hr_collecte AS (
    SELECT
        'collecte' AS type,
        id_collecte AS id_stat,
        id_agent_1_id AS id_agent,
        date_collecte AS date,
        a1_hr_debut AS hr_debut,
        a1_hr_fin AS hr_fin,
        '' AS presence
    FROM core_collecte
    WHERE id_agent_1_id IS NOT NULL

    UNION ALL

    SELECT
        'collecte' AS type,
        id_collecte AS id_stat,
        id_agent_2_id AS id_agent,
        date_collecte AS date,
        a2_hr_debut AS hr_debut,
        a2_hr_fin AS hr_fin,
        '' AS presence
    FROM core_collecte
    WHERE id_agent_2_id IS NOT NULL

    UNION ALL

    SELECT
        'collecte' AS type,
        id_collecte AS id_stat,
        id_agent_3_id AS id_agent,
        date_collecte AS date,
        a3_hr_debut AS hr_debut,
        a3_hr_fin AS hr_fin,
        '' AS presence
    FROM core_collecte
    WHERE id_agent_3_id IS NOT NULL
),
entries AS (
    SELECT * FROM hr_collecte
    UNION ALL
    SELECT * FROM hr_manuelles
)
SELECT
    id_agent,
    date,
    type,
    id_stat,
    CASE
        WHEN COALESCE(NULLIF(BTRIM(presence), ''), '') <> '' THEN presence
        WHEN hr_fin IS NOT NULL THEN TO_CHAR(hr_fin, 'HH24:MI')
        ELSE ''
    END AS stat
FROM entries;
"""


def main() -> None:
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME", "bdd_regie"),
        user=os.getenv("DB_USER", "super_user"),
        password=os.getenv("DB_PASSWORD", ""),
        host=os.getenv("DB_HOST", "db"),
        port=int(os.getenv("DB_PORT", "5432")),
    )

    try:
        with conn.cursor() as cursor:
            cursor.execute(req_view_stat_collectes)
        conn.commit()
        print("Vue PostgreSQL creee/mise a jour: req_view_stat_collectes")
    finally:
        conn.close()


if __name__ == "__main__":
    main()
