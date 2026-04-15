WITH dates AS (
    SELECT generate_series(
        DATE '2026-01-01',
        DATE '2026-04-14',
        INTERVAL '1 day'
    )::date AS date
),
agents AS (
    SELECT 
        id,
        arrivee, 
        depart 
    FROM core_agent
)
SELECT 
    a.id id_agent,
    d.date,
    a.id id_stat,
    CASE 
    WHEN (
        d.date >= a.arrivee 
        AND (a.depart IS NULL OR d.date <= a.depart)
    )
    THEN 'contrat_ok'
    ELSE 'contrat_off'
END AS type,
    null::int4 id_flux,
    null::int8 id_itineraire,
    false is_heures_sup,
    null::time AS hr_debut,
    null::time AS hr_fin,
    null::text as motif_hs,
    null::int8 as presence_id
FROM dates d
CROSS JOIN agents a
ORDER BY d.date, a.id;