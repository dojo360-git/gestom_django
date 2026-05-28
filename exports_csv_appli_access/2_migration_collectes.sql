/*  
 * 2_migration_collectes.sql
 * migration des collectes 2026-05-28
 */



TRUNCATE TABLE core_collecte RESTART IDENTITY;

INSERT INTO core_collecte (
    id_collecte, date_collecte,
    a1_hr_debut, a1_hr_fin,
    a2_hr_debut, a2_hr_fin,
    a3_hr_debut, a3_hr_fin,
    motif_heures_sup,
    hr_sup_debut, hr_sup_fin,
    km_depart, km_retour,
    hr_depot_depart, hr_depot_retour,
    tonnage1, tonnage2, tonnage3,
    energie_qte_1,
    consignes,
    info_vehicule,
    info_collecte,
    date_creation, date_modification,
    id_agent_1_id, id_agent_2_id, id_agent_3_id,
    id_flux1_id, id_flux2_id, id_flux3_id,
    id_itineraire_id,
    id_vehicule_id
)
SELECT DISTINCT ON (id_collecte)
    id_collecte,
    COALESCE(date_collecte, CURRENT_DATE),
    a1_hr_debut, a1_hr_fin,
    a2_hr_debut, a2_hr_fin,
    a3_hr_debut, a3_hr_fin,
    motif_heures_sup,
    hr_sup_debut, hr_sup_fin,
    km_depart, km_retour,
    hr_depot_depart, hr_depot_retour,
    tonnage1*1000 tonnage1, tonnage2*1000 tonnage2, tonnage3*1000 tonnage3,
    energie_qte_1,
    COALESCE(consignes, ''),
    COALESCE(info_vehicule, ''),
    COALESCE(info_collecte, ''),
    COALESCE(date_creation, NOW()),
    COALESCE(date_modification, NOW()),
    id_agent_1_id, id_agent_2_id, id_agent_3_id,
    id_flux1_id, id_flux2_id, id_flux3_id,
    id_itineraire_id,
    id_vehicule_id
FROM preprod_core_collecte
ORDER BY id_collecte, date_modification DESC NULLS LAST;

SELECT setval(
    pg_get_serial_sequence('core_collecte', 'id_collecte'),
    COALESCE(MAX(id_collecte), 1)
)
FROM core_collecte;