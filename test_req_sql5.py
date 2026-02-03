import sqlite3
import json

conn = sqlite3.connect("db.sqlite3")
conn.row_factory = sqlite3.Row   # 👈 important
cursor = conn.cursor()


# python test_req_sql5.py


cursor.execute("""
    WITH  
               
cflux AS (
    SELECT *
    FROM core_flux
),

tournees AS (
    SELECT
        id_collecte,
        COALESCE(km_retour - km_depart, 0) AS km_tournee,
        COALESCE(tonnage1, 0) + COALESCE(tonnage2, 0) + COALESCE(tonnage3, 0) AS tonnage_tournee,
        id_energie_1_id id_energie_1, 
        id_energie_2_id id_energie_2, 
        id_energie_3_id id_energie_3, 
        energie_qte_1 energie_qte_1_tournee, 
        energie_qte_2 energie_qte_2_tournee, 
        energie_qte_3 energie_qte_3_tournee 
               

    FROM core_collecte
),

vidages AS (
    SELECT
        t.id_collecte,
        t.date_collecte,
        t.id_flux,
        t.tonnage
    FROM (
        SELECT id_collecte, date_collecte, id_flux1_id AS id_flux, tonnage1 AS tonnage
        FROM core_collecte
        WHERE tonnage1 IS NOT NULL

        UNION ALL
        SELECT id_collecte, date_collecte, id_flux2_id AS id_flux, tonnage2 AS tonnage
        FROM core_collecte
        WHERE tonnage2 IS NOT NULL

        UNION ALL
        SELECT id_collecte, date_collecte, id_flux3_id AS id_flux, tonnage3 AS tonnage
        FROM core_collecte
        WHERE tonnage3 IS NOT NULL
    ) t
    --LEFT JOIN cflux f ON t.id_flux = f.id_flux
),

               
    vidages2 as (
    SELECT
        v.id_collecte,
        v.date_collecte,
        v.id_flux,
        v.tonnage,
        tr.km_tournee,
        tr.tonnage_tournee,
        id_energie_1,
        id_energie_2,
        id_energie_3,
        energie_qte_1_tournee,
        energie_qte_2_tournee,
        energie_qte_3_tournee,
        CASE
            WHEN NULLIF(tr.tonnage_tournee, 0) IS NULL THEN 0
            ELSE round( (v.tonnage / NULLIF(tr.tonnage_tournee, 0)),6) -- tr.km_tournee * (v.tonnage / NULLIF(tr.tonnage_tournee, 0))
        END AS ventil
    FROM vidages v
    LEFT JOIN tournees tr ON tr.id_collecte = v.id_collecte
    )
               
    SELECT 
        *,
        round(km_tournee * ventil,2) km,
        round(energie_qte_1_tournee * ventil,2)  energie_qte_1,
        round(energie_qte_2_tournee * ventil,2)  energie_qte_2,
        round(energie_qte_3_tournee * ventil,2)  energie_qte_3


    FROM vidages2;
""")

rows = cursor.fetchall()

# ➜ sqlite3.Row -> dict
data = []
for r in rows:
    #if r["id_flux"] is None or r["tonnage"] is None:
    #    continue
    data.append(dict(r))

print(rows)
json_data = json.dumps(data, indent=2, ensure_ascii=False)
print(json_data)

conn.close()


# ['id_collecte', 
#  'date_collecte', 
#  'a1_hr_debut', 
#  'a1_hr_fin', 
#  'a2_hr_debut', 
#  'a2_hr_fin', 
#  'a3_hr_debut', 
#  'a3_hr_fin', 
#  'km_depart', 
#  'km_retour', 
#  'tonnage1', 
#  'tonnage2', 
#  'tonnage3', 
#  'energie_qte_1', 
#  'energie_qte_2', 
#  'energie_qte_3', 
#  'date_creation', 
#  'date_modification', 
#  'id_agent_1_id', 
#  'id_agent_2_id', 
#  'id_agent_3_id', 
#  'id_energie_1_id', 
#  'id_energie_2_id', 
#  'id_energie_3_id', 
#  'id_flux1_id', 
#  'id_flux2_id', 
#  'id_flux3_id', 
#  'id_vehicule_id']