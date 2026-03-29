import sqlite3
import json

conn = sqlite3.connect("db.sqlite3")
conn.row_factory = sqlite3.Row   # 👈 important
cursor = conn.cursor()

cursor.execute("""
WITH cflux AS (
    SELECT  *
    FROM core_flux
)
SELECT 
    tonnages.date_collecte,
    cflux.flux,
    sum(tonnages.tonnage)/1000 as tonnage


FROM (
    SELECT 
        id_collecte, 
        date_collecte,
        id_flux1_id AS id_flux, 
        tonnage1 AS tonnage
    FROM core_collecte
    WHERE tonnage1 is not null

    UNION ALL 

    SELECT
        id_collecte, 
        date_collecte,
        id_flux2_id AS id_flux, 
        tonnage2 AS tonnage
    FROM core_collecte
    WHERE tonnage2 is not null

    UNION ALL 

    SELECT 
        id_collecte,
        date_collecte,
        id_flux3_id AS id_flux, 
        tonnage3 AS tonnage
    FROM core_collecte
    WHERE tonnage3 is not null
) tonnages
LEFT JOIN cflux ON tonnages.id_flux = cflux.id_flux
GROUP BY 1,2
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


# colonnes_core_collecte = 
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