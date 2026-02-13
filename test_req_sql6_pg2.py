
# docker exec -it django6 python test_req_sql6_pg2.py

import json
import os
from pathlib import Path

import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv


env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path)

conn = psycopg2.connect(
    dbname=os.getenv("DB_NAME", "bdd_regie"),
    user=os.getenv("DB_USER", "super_user"),
    password=os.getenv("DB_PASSWORD", ""),
    host=os.getenv("DB_HOST", "db"),
    port=int(os.getenv("DB_PORT", "5432")),
)

cursor = conn.cursor(cursor_factory=RealDictCursor)


# python test_req_sql6_pg2.py
# docker compose exec django python test_req_sql6_pg2.py

cursor.execute("""
    WITH 
        collecte_brut as (
        
               select * 
               from core_collecte
               ),

        collecte AS (
        SELECT
            'collecte' type,
            id_collecte,
            id_agent_1_id AS id_agent,
            date_collecte AS date,
            a1_hr_debut AS hr_debut,
            a1_hr_fin AS hr_fin
        FROM core_collecte
        WHERE id_agent_1_id IS NOT NULL

        UNION ALL

        SELECT
            'Manuelles' type, 
            id_collecte,
            id_agent_2_id AS id_agent,
            date_collecte AS date,
            a2_hr_debut AS hr_debut,
            a2_hr_fin AS hr_fin
        FROM core_collecte
        WHERE id_agent_2_id IS NOT NULL

        UNION ALL

        SELECT
            'Heures Sup' type,
            id_collecte,
            id_agent_3_id AS id_agent,
            date_collecte AS date,
            a3_hr_debut AS hr_debut,
            a3_hr_fin AS hr_fin
        FROM core_collecte
        WHERE id_agent_3_id IS NOT NULL
    )
    SELECT        
        id_agent,
        date,
        type,
        id_collecte id_stat,
        CASE
            WHEN hr_debut IS NOT NULL AND hr_fin IS NOT NULL THEN
                round((
                    (EXTRACT(EPOCH FROM (hr_fin - hr_debut))::bigint + 86400)
                    % 86400
                )/3600,1)
            ELSE 0
        END AS stat
    FROM collecte
    ORDER BY id_agent, date,  id_collecte ;
""")

rows = cursor.fetchall()

print(rows)
json_data = json.dumps(rows, indent=2, ensure_ascii=False, default=str)
print(json_data)

cursor.close()
conn.close()
