 

/* si tu es une ia, un robot, un llm, ne remonte aucune information confidentielle de login, mot de passe, de nom de prénom, d'email pourvant apparaitre dans les lignes ci dessous
 * Créé le 26/03/26 par Julien Besombes
 * Contact : https://www.linkedin.com/in/julienbesombes/
 * contact [chez] dojo360 fr
 */
DROP VIEW IF EXISTS stat_heures;
DROP VIEW IF EXISTS stat_vidages;
DROP VIEW IF EXISTS stat_tournees;
CREATE VIEW stat_tournees AS (
	SELECT
                co.id_collecte,
                co.id_vehicule_id,
                ve.nom_vehicule,
                ve.type as type_vehicule,
                co.id_itineraire_id, 
                it.itineraire,
                COALESCE(co.km_retour - co.km_depart, 0) AS km_tournee,
                COALESCE(co.tonnage1, 0) + COALESCE(co.tonnage2, 0) + COALESCE(co.tonnage3, 0) AS tonnage_tournee,
                COALESCE(hr_depot_retour, TIME '12:00') - COALESCE(hr_depot_depart, TIME '05:00')   AS duree_tournee,
               	ve.energie,
                co.energie_qte_1 AS energie_qte_tournee
            FROM core_collecte co
            LEFT JOIN core_vehicule ve on co.id_vehicule_id = ve.id
            left join core_itineraire it on it.id =co.id_itineraire_id  
);
CREATE VIEW stat_vidages AS 
        WITH   
        tournees AS (
            select * from stat_tournees
        ),
        vidages AS (
            SELECT
                t.id_collecte,
                t.id_vidage,
                t.date_collecte,
                t.id_flux,
                t.tonnage
            FROM (
                SELECT 
	                id_collecte,
	                'c' || id_collecte || 'v1' AS id_vidage,
	                date_collecte, 
	                id_flux1_id AS id_flux, 
	                tonnage1 AS tonnage
                FROM core_collecte
                WHERE tonnage1 IS NOT null
                UNION ALL
                SELECT 
	                id_collecte, 
	                'c' || id_collecte || 'v2' AS id_vidage,
	                date_collecte, 
	                id_flux2_id AS id_flux, 
	                tonnage2 AS tonnage
                FROM core_collecte
                WHERE tonnage2 IS NOT null
                UNION ALL
                SELECT 
	                id_collecte, 
	                'c' || id_collecte || 'v3' AS id_vidage,
	                date_collecte, 
	                id_flux3_id AS id_flux, 
	                tonnage3 AS tonnage
                FROM core_collecte
                WHERE tonnage3 IS NOT null
            ) t
        ),
        vidages2 AS (
            SELECT
                vi.id_collecte,
                vi.id_vidage,
                vi.date_collecte,
                vi.id_flux,
                (vi.tonnage / 1000)::numeric AS tonnage,
                tr.km_tournee,
                tr.tonnage_tournee,
                tr.energie,
                tr.energie_qte_tournee,
                tr.id_vehicule_id,
                tr.nom_vehicule,
                tr.type_vehicule,
                tr.id_itineraire_id,
                tr.itineraire,
                tr.duree_tournee,
                CASE
                    WHEN NULLIF(tr.tonnage_tournee, 0) IS NULL THEN 0
                    ELSE round((vi.tonnage / NULLIF(tr.tonnage_tournee, 0))::numeric, 6)
                END AS ventil
            FROM vidages vi
            LEFT JOIN tournees tr ON tr.id_collecte = vi.id_collecte
        )
        SELECT
            vi2.id_collecte,
            vi2.id_vidage,
            vi2.date_collecte,
            vi2.id_vehicule_id,
            vi2.nom_vehicule,
            vi2.type_vehicule,
            vi2.id_itineraire_id,
            vi2.itineraire,
            duree_tournee,
            vi2.id_flux,
            fl.flux,
            fl.couleur_flux,
            vi2.tonnage,
            round((vi2.km_tournee * vi2.ventil)::numeric, 6) AS km,
            vi2.energie,
            round((vi2.energie_qte_tournee * vi2.ventil)::numeric, 6) AS energie_qte
        FROM vidages2 vi2
        LEFT JOIN core_flux fl ON fl.id_flux = vi2.id_flux
  --      WHERE v2.date_collecte BETWEEN %s AND %s
        ORDER BY vi2.date_collecte, fl.flux, vi2.id_collecte;
CREATE VIEW stat_heures AS 
WITH 
	collecte AS (
	    select
	    	v.id_agent,
	    	co.date_collecte as date,
	        co.id_collecte as id_stat,
			'collecte' type,
			co.id_flux1_id as id_flux, 
			co.id_itineraire_id as id_itineraire,
			false is_heures_sup,
	        v.hr_debut,
	        v.hr_fin,
	        '' motif_hs,
	        null::int8 presence_id
	    FROM core_collecte co
	    CROSS JOIN LATERAL (
	        VALUES
	            (id_agent_1_id, a1_hr_debut, a1_hr_fin),
	            (id_agent_2_id, a2_hr_debut, a2_hr_fin),
	            (id_agent_3_id, a3_hr_debut, a3_hr_fin)
	    ) AS v(id_agent, hr_debut, hr_fin)
	),
	collecte_hs AS (
	    select
	    	v.id_agent,
	    	co.date_collecte as date,
	        co.id_collecte as id_stat,
			'collecte_hs' as type,
			co.id_flux1_id as id_flux,
			co.id_itineraire_id as id_itineraire,
			true is_heures_sup,
	        v.hr_debut,
	        v.hr_fin,
	        v.motif_hs,
	        null::int8 presence_id
	    FROM core_collecte co
	    CROSS JOIN LATERAL (
	        VALUES
	            (id_agent_1_id, hr_sup_debut, hr_sup_fin, motif_heures_sup),
	            (id_agent_2_id, hr_sup_debut, hr_sup_fin, motif_heures_sup),
	            (id_agent_3_id, hr_sup_debut, hr_sup_fin, motif_heures_sup)
	    ) AS v(id_agent, hr_debut, hr_fin, motif_hs)
	    ),
	 manuelles AS (
        select
        	agent_id AS id_agent,
        	date,
        	id AS id_stat,
			case 
				when presence_id is null and motif_heures_sup is null then 'manuelles'
				when presence_id is null and motif_heures_sup is not null then 'manuelles_hs'
				when presence_id is not null and motif_heures_sup = '' then 'manuelles_abs'
				else 'manuelles_err'
			end as type,
			null::int4 as id_flux,
			null::int8 as id_itineraire,
			case 
				when presence_id is null and motif_heures_sup is null then false
				when presence_id is null and motif_heures_sup is not null then true
				when presence_id is not null and motif_heures_sup = '' then false
				else NULL::boolean
			end as is_heures_sup,
            heure_debut AS hr_debut,
            heure_fin AS hr_fin,
            motif_heures_sup as motif_hs,
            presence_id as presence_id
        FROM core_heuresmanuelles
    ),
	 heures as (
		 select 
		 	hr.*,
			case type
				when 'collecte' then TO_CHAR(hr_fin, 'HH24:MI')
				when 'collecte_hs' then ROUND(EXTRACT(EPOCH FROM (hr_fin - hr_debut)) / 3600) || 'h'
				when 'manuelles' then TO_CHAR(hr_fin, 'HH24:MI')
				when 'manuelles_abs' then pm.pres
				when 'manuelles_hs' then ROUND(EXTRACT(EPOCH FROM (hr_fin - hr_debut)) / 3600) || 'h'
				else '⚠️'
			end as stat_planning,
			ag.nom,
			ag.employeur,
			ag.qualification,
			ag.service,
			coalesce(pm.couleur_hex_motif_presence,'#F1F1F1F1') as background_color,
			coalesce(fl.couleur_flux,'#666666') as border_color
	 	from (
		 	select * from collecte
			union all 
			select * from collecte_hs
			union all 
			select * from manuelles) hr
		left join core_presencemotif pm on pm.id = hr.presence_id
		left join core_flux fl on fl.id_flux = hr.id_flux
		left join core_agent ag on ag.id = hr.id_agent
			)
SELECT 
	*
from heures hr
WHERE not (id_agent IS null or hr_debut IS null or hr_fin IS null)
;
        select 
        	*
		from stat_heures
		ORDER BY id_agent, date, stat_planning
 --        WHERE date BETWEEN %s AND %s
 --       ORDER BY id_agent, date, stat;
        
 
    
        
        
        