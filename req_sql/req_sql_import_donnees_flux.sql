UPDATE public.core_collecte
SET id_itineraire_id = 17
WHERE tonnage1 > 2000
  AND date_collecte >= '2026-01-01'
  --AND date_collecte < '2026-06-02';