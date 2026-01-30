import sqlite3
import json

conn = sqlite3.connect("db.sqlite3")
conn.row_factory = sqlite3.Row   # 👈 important
cursor = conn.cursor()

cursor.execute("""
WITH collecte AS (
    SELECT *,
    "collecte" type 
               

    FROM (

    SELECT 
        id_agent_1_id  id_agent, 
        date_collecte date,
        a1_hr_debut AS hr_debut, 
        a1_hr_fin AS hr_fin
    FROM core_collecte
    WHERE id_agent_1_id is not null

    UNION ALL 

    SELECT
        id_agent_2_id id_agent, 
        date_collecte date,
        a2_hr_debut AS hr_debut, 
        a2_hr_fin AS hr_fin
    FROM core_collecte
    WHERE tonnage2 is not null

    UNION ALL 

    SELECT 
        id_agent_3_id id_agent,
        date_collecte date,
        a3_hr_debut AS hr_debut, 
        a3_hr_fin AS hr_fin
    FROM core_collecte
    )
)
SELECT 
    *
FROM collecte
""")

rows = cursor.fetchall()

# ➜ sqlite3.Row -> dict
data = []
for r in rows:
    #if r["id_flux"] is None or r["tonnage"] is None:
    #    continue
    data.append(dict(r))

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