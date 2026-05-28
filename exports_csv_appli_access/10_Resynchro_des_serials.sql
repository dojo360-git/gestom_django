-- 10_Resynchro_des_serials.sql

SELECT setval(
    pg_get_serial_sequence('core_agent', 'id'),
    COALESCE(MAX(id), 1)
)
FROM core_agent;

SELECT setval(
    pg_get_serial_sequence('core_collecte', 'id_collecte'),
    COALESCE(MAX(id_collecte), 1)
)
FROM core_collecte;

SELECT setval(
    pg_get_serial_sequence('core_energie', 'id'),
    COALESCE(MAX(id), 1)
)
FROM core_energie;

SELECT setval(
    pg_get_serial_sequence('core_flux', 'id_flux'),
    COALESCE(MAX(id_flux), 1)
)
FROM core_flux;

SELECT setval(
    pg_get_serial_sequence('core_heuresmanuelles', 'id'),
    COALESCE(MAX(id), 1)
)
FROM core_heuresmanuelles;

SELECT setval(
    pg_get_serial_sequence('core_itineraire', 'id'),
    COALESCE(MAX(id), 1)
)
FROM core_itineraire;

SELECT setval(
    pg_get_serial_sequence('core_parametre', 'id'),
    COALESCE(MAX(id), 1)
)
FROM core_parametre;

SELECT setval(
    pg_get_serial_sequence('core_presencemotif', 'id'),
    COALESCE(MAX(id), 1)
)
FROM core_presencemotif;

SELECT setval(
    pg_get_serial_sequence('core_vehicule', 'id'),
    COALESCE(MAX(id), 1)
)
FROM core_vehicule;

--core_agent id
--core_collecte id_collecte
--core_energie id
--core_flux id_flux
--core_heuresmanuelles id
--core_itineraire id
--core_parametre id
--core_presencemotif id
--core_vehicule id