/*  
 * 3_migr_heures_manuelles.sql
 * migration des collectes 2026-05-28
 */

DROP TABLE IF EXISTS preprod_core_heuresmanuelles;
CREATE TABLE preprod_core_heuresmanuelles AS
--SELECT *
--FROM core_heuresmanuelles;
--TRUNCATE TABLE core_heuresmanuelles RESTART IDENTITY;


CREATE TABLE preprod_core_heuresmanuelles as 
(

with  agents as (
	SELECT 
		id, 
		nom 
		--prenom, 
		--qualification, 
		--service, 
		--employeur, 
		--hds_defaut, 
		--hfs_defaut, 
		--echeance_permis, 
		--echeance_fco, 
		--arrivee, 
		--depart, 
		--tel
	FROM public.core_agent ag ),

tb_planning as (
	SELECT 
		"IdPlan", 
		"DatePlan", 
		"NomAgentPlan" ag, 
		"HFSAgentPlan", 
		"HSupAgentPlan", 
		"MotifHSPlan", 
		"TRPlan", 
		"MotifAbsPlan",
		"HDebutPlan", 
		"ObsPlan",
		pm.id id_motif_pres,
		ag.id id_agent,
		"IdTourneePlan" id_collecte
	FROM public."zzz_Tb_Planning" tbp
	LEFT JOIN (
		SELECT 
		id, 
		pres
		--presence, 
		--jour_travail, 
		--couleur_hex_motif_presence, 
		--date_creation, 
		--date_modification
		FROM public.core_presencemotif pm
		) pm 
	ON pm.pres = tbp."MotifAbsPlan"	
	LEFT JOIN agents ag
	ON ag.nom = tbp."NomAgentPlan"),
	
	
	
	
	
	tb_planning_abs AS (
	SELECT 
	*,
	'manuelles_abs' type
	FROM tb_planning tbp
	WHERE NOT  ("MotifAbsPlan" is null or "MotifAbsPlan" = '')),
	
	
	tb_planning_manuelles AS (
	SELECT *,
	'manuelles' type
	FROM tb_planning tbp
	WHERE   id_collecte is null and ("MotifAbsPlan" is null or "MotifAbsPlan" = '') 
	),
	
	tb_planning_manuelles_hs AS (
	SELECT *,
	'manuelles_hs' type
	FROM tb_planning tbp
	WHERE   id_collecte is null and "HSupAgentPlan" > '00:00:00'
	),
	
	
	
	
	migr_heuresmanuelles_abs as (
	SELECT 
		"IdPlan" id_old, 
		tbp."DatePlan" "date", 
		"HDebutPlan" heure_debut, 
		"HFSAgentPlan" heure_fin, 
		'' motif_heures_sup, 
		tbp."DatePlan" date_creation, 
		tbp."DatePlan" date_modification, 
		id_agent agent_id, 
		id_motif_pres presence_id,
		type
	FROM tb_planning_abs tbp
),
	
	migr_heuresmanuelles_manuelles as (
	SELECT 
		"IdPlan" id_old, 
		tbp."DatePlan" "date", 
		"HDebutPlan" heure_debut, 
		"HFSAgentPlan" heure_fin, 
		'' motif_heures_sup, 
		tbp."DatePlan" date_creation, 
		tbp."DatePlan" date_modification, 
		id_agent agent_id, 
		id_motif_pres presence_id,
		type
		FROM tb_planning_manuelles tbp
),
	

	migr_heuresmanuelles_manuelles_hs as (
	SELECT 
		"IdPlan" id_old, 
		tbp."DatePlan" "date", 
		"HDebutPlan" heure_debut, 
		"HFSAgentPlan" heure_fin, 
		'' motif_heures_sup, 
		tbp."DatePlan" date_creation, 
		tbp."DatePlan" date_modification, 
		id_agent agent_id, 
		id_motif_pres presence_id,
		type
		FROM tb_planning_manuelles_hs tbp
),


migr_heuresmanuelles AS (

    SELECT *
    FROM (
        SELECT * FROM migr_heuresmanuelles_abs
        UNION ALL
        SELECT * FROM migr_heuresmanuelles_manuelles
        UNION ALL
        SELECT * FROM migr_heuresmanuelles_manuelles_hs
    ) t
    -- WHERE id_old IN (21310, 21355, 24938, 26459) collecte erreur 
    ORDER BY id_old

)
	
	
	

	select * 
	 from migr_heuresmanuelles



)