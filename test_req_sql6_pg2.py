
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

    hr_manuelles as (
        SELECT 
            'Manuelles' type,
            id id_stat,
            agent_id AS id_agent,
            date AS date,
            heure_debut AS hr_debut,
            heure_fin AS hr_fin,
            presence
        FROM core_heuresmanuelles
        WHERE motif_heures_sup is null
            ),

    hr_sup as (
        SELECT 
            'Heures Sup' type,
            id id_stat,
            agent_id AS id_agent,
            date AS date,
            heure_debut AS hr_debut,
            heure_fin AS hr_fin,
            presence 
        FROM core_heuresmanuelles
        WHERE motif_heures_sup is not null
            ),
            

        hr_collecte_1 AS (
        SELECT
            'collecte' type,
            id_collecte,
            id_agent_1_id AS id_agent,
            date_collecte AS date,
            a1_hr_debut AS hr_debut,
            a1_hr_fin AS hr_fin,
            '' presence
        FROM core_collecte
        WHERE id_agent_1_id IS NOT NULL

        UNION ALL

        SELECT
            'collecte' type, 
            id_collecte,
            id_agent_2_id AS id_agent,
            date_collecte AS date,
            a2_hr_debut AS hr_debut,
            a2_hr_fin AS hr_fin,
            '' presence
        FROM core_collecte
        WHERE id_agent_2_id IS NOT NULL

        UNION ALL

        SELECT
            'collecte' type,
            id_collecte,
            id_agent_3_id AS id_agent,
            date_collecte AS date,
            a3_hr_debut AS hr_debut,
            a3_hr_fin AS hr_fin,
            '' presence
        FROM core_collecte
        WHERE id_agent_3_id IS NOT NULL
               
        UNION ALL
                
        SELECT * 
        FROM hr_manuelles
                
        UNION ALL
                
        SELECT * 
        FROM hr_sup
               



    ),
               
    hr_collecte_2 as (
    SELECT        
        id_agent,
        date,
        type,
        id_collecte id_stat,
        TO_CHAR(hr_fin, 'HH24:MI') as stat,
        --CASE
        --    WHEN hr_debut IS NOT NULL AND hr_fin IS NOT NULL THEN
        --        round((
        --            (EXTRACT(EPOCH FROM (hr_fin - hr_debut))::bigint + 86400)
        --            % 86400
        --        )/3600,1)
        --    ELSE 0
        -- END AS stat,
        presence
    FROM hr_collecte_1
    ORDER BY id_agent, date,  hr_debut )
               


               
    SELECT 
        id_agent,
        date,
        type,
        id_stat,
        CASE 
            WHEN presence <> '' THEN presence
            WHEN presence is not Null  THEN stat::TEXT 
            ELSE presence
        END AS stat 
    FROM hr_collecte_2
    

               
               ;

""")

rows = cursor.fetchall()

print(rows)
json_data = json.dumps(rows, indent=2, ensure_ascii=False, default=str)
print(json_data)

cursor.close()
conn.close()
