
DROP TABLE IF EXISTS preprod_core_collecte;
CREATE TABLE preprod_core_collecte AS
SELECT *
FROM core_collecte;

DROP TABLE IF EXISTS preprod_core_heuresmanuelles;
CREATE TABLE preprod_core_heuresmanuelles AS
SELECT *
FROM core_heuresmanuelles;


with agents as (
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
	FROM public.core_agent ag 
),
collectes as (
SELECT  
	id_collecte, 
	date_collecte, 
	a1_hr_debut, 
	a1_hr_fin, 
	a2_hr_debut, 
	a2_hr_fin, 
	a3_hr_debut, 
	a3_hr_fin, 
	motif_heures_sup, 
	hr_sup_debut, 
	hr_sup_fin, 
	km_depart, 
	km_retour, 
	hr_depot_depart, 
	hr_depot_retour, 
	tonnage1, 
	tonnage2, 
	tonnage3, 
	energie_qte_1, 
	consignes, 
	info_vehicule, 
	info_collecte, 
	date_creation, 
	date_modification, 
	id_agent_1_id, 
	id_agent_2_id, 
	id_agent_3_id, 
	id_flux1_id, 
	id_flux2_id, 
	id_flux3_id, 
	id_itineraire_id, 
	id_vehicule_id
FROM public.core_collecte
),

planning as (
SELECT 
	"IdPlan", 
	"DatePlan", 
	"NomAgentPlan", 
	"HFSAgentPlan", 
	"HSupAgentPlan", 
	"MotifHSPlan", 
	"TRPlan", 
	"MotifAbsPlan", 
	"IdTourneePlan", 
	"HDebutPlan", 
	"ObsPlan"
FROM public."zzz_Tb_Planning"
),

planning_tournees as (
select * 
from planning
where is not null
) ,


fx as (
SELECT 
	id_flux, 
	flux 
	--flux_long, 
	--couleur_flux, 
	--archive
FROM public.core_flux)




/*
 
IdTou id_collecte, 
DateTou date_collecte, 
NumTou, 
AmPmTou, 
FluxTou, 
ChauffeurTou, 
Ripeur1Tou, 
Ripeur2Tou, 
VehiculeTou, 
T1Tou, 
T2Tou, 
Champ1, 
T3Tou, 
CarburantTou, 
QCarbTou, 
QAdBlueTou, 
KmTou, 
HFSTou, 
HSupTou, 
MotifHSupTou, 
ServiceTou
 */

SELECT 
	tbt."IdTou" id_collecte, 
	tbt."DateTou" date_collecte, 
--	a1_hr_debut, 
--	a1_hr_fin, 
--	a2_hr_debut, 
--	a2_hr_fin, 
--	a3_hr_debut, 
--	a3_hr_fin, 
	tbt."MotifHSupTou"	motif_heures_sup, 
	'12:00:00'::time hr_sup_debut, 
	'12:00:00'::time + "HSupTou"::interval hr_sup_fin, 
	0	km_depart, 
	tbt."KmTou" km_retour, 
--	hr_depot_depart, 
--	hr_depot_retour, 
	tbt."T1Tou" tonnage1, 
	tbt."T2Tou" tonnage2, 
	tbt."T3Tou" tonnage3, 
	"QCarbTou" energie_qte_1, 
	null::varchar  consignes, 
	null::varchar info_vehicule, 
	null::varchar info_collecte, 
	"DateTou" date_creation, 
	"DateTou" date_modification, 
	ag1.id id_agent_1_id, 
	ag2.id id_agent_2_id, 
	ag3.id id_agent_3_id, 
	fx."id_flux"	id_flux1_id, 
	fx."id_flux" 	id_flux2_id, 
	fx."id_flux"	id_flux3_id, 
	null::int8 id_itineraire_id,
	1 id_vehicule_id,
	tbt."FluxTou" test
FROM public."zzz_Tb_Tournee" tbt
left join agents ag1 on ag1.nom = tbt."ChauffeurTou"
left join agents ag2 on ag2.nom = tbt."Ripeur1Tou" 
left join agents ag3 on ag3.nom = tbt."Ripeur2Tou" 
left join fx  on fx.flux = tbt."FluxTou"
-- limit;




;