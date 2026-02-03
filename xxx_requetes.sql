 WITH 
        
        cflux AS (
            SELECT *
            FROM core_flux
        ), 
               
        tournees AS (
            SELECT 
                id_collecte,
                COALESCE(km_retour - km_depart,0) km_tournee,
                COALESCE(tonnage1,0) + COALESCE(tonnage2,0) + COALESCE(tonnage3,0) tonnage_tournee
            FROM core_collecte), 
            
                    
        vidages AS (
               
        SELECT
            id_collecte,
            cflux.flux,
            tonnages.tonnage
            --SUM(tonnages.tonnage) / 1000.0 AS tonnage,
            --COUNT(*) AS nb_vidages,
            --COUNT(DISTINCT tonnages.id_collecte) AS nb_tournees,
            --SUM(tonnages.tonnage) / 1000.0 / NULLIF(COUNT(*), 0) AS tonnage_moyen
        FROM (
            SELECT
                id_collecte,
                date_collecte,
                id_flux1_id AS id_flux,
                tonnage1 AS tonnage
            FROM core_collecte
            WHERE tonnage1 IS NOT NULL

            UNION ALL

            SELECT
                id_collecte,
                date_collecte,
                id_flux2_id AS id_flux,
                tonnage2 AS tonnage
            FROM core_collecte
            WHERE tonnage2 IS NOT NULL

            UNION ALL

            SELECT
                id_collecte,
                date_collecte,
                id_flux3_id AS id_flux,
                tonnage3 AS tonnage
            FROM core_collecte
            WHERE tonnage3 IS NOT NULL
        ) t
        
        LEFT JOIN cflux f ON t.id_flux = f.id_flux
        --WHERE tonnages.date_collecte BETWEEN %s AND %s
        --GROUP BY cflux.flux
        --ORDER BY cflux.flux
               )
               
        SELECT 
            v.id_collecte,
             -- km_tournee * tonnage / tonnage_tournee km 
                
        FROM vidages v
        LEFT JOIN tournees t on t.id_collecte = v.id_collecte











    WITH
cflux AS (
    SELECT *
    FROM core_flux
),

tournees AS (
    SELECT
        id_collecte,
        COALESCE(km_retour - km_depart, 0) AS km_tournee,
        COALESCE(tonnage1, 0) + COALESCE(tonnage2, 0) + COALESCE(tonnage3, 0) AS tonnage_tournee
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
)

SELECT
    v.id_collecte,
    v.date_collecte,
    v.id_flux,
    --f.flux,
    v.tonnage,
    tr.km_tournee,
    tr.tonnage_tournee,
    
    CASE
        WHEN NULLIF(tr.tonnage_tournee, 0) IS NULL THEN 0
        ELSE  (v.tonnage / NULLIF(tr.tonnage_tournee, 0)) --tr.km_tournee * (v.tonnage / NULLIF(tr.tonnage_tournee, 0))
    END AS ventil
FROM vidages v
LEFT JOIN tournees tr ON tr.id_collecte = v.id_collecte
LEFT JOIN cflux f ON t.id_flux = f.id_flux;