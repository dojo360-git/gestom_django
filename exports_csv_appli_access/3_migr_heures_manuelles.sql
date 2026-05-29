/*  
 * 3_migr_heures_manuelles.sql
 * migration des collectes 2026-05-28
 */


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
	SELECT *
	FROM tb_planning tbp
	WHERE NOT  ("MotifAbsPlan" is null or "MotifAbsPlan" = '')),
	
	
	tb_planning_heuresmanuelles AS (
	SELECT *
	FROM tb_planning tbp
	WHERE   id_collecte is null and "HFSAgentPlan" = '00:00:00'::time
	),
	
	
	migr_heuresmanuelles_abs as (
	SELECT 
		--id, 
		tbp."DatePlan" "date", 
		"HDebutPlan" heure_debut, 
		"HFSAgentPlan" heure_fin, 
		'' motif_heures_sup, 
		tbp."DatePlan" date_creation, 
		tbp."DatePlan" date_modification, 
		id_agent agent_id, 
		id_motif_pres presence_id
	FROM tb_planning_abs tbp
)
	
	
	select * from tb_planning_heuresmanuelles