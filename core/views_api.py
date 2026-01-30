from django.http import JsonResponse
from django.db import connection
from django.views.decorators.http import require_GET

@require_GET
def tonnages_json(request):
    #date_from = request.GET.get("date_from")
    #date_to = request.GET.get("date_to")

    sql = """
    WITH cflux AS (
        SELECT *
        FROM core_flux
    )
    SELECT
        tonnages.date_collecte,
        cflux.flux,
        SUM(tonnages.tonnage)/1000.0 AS tonnage,
        COUNT(*) as NbVidages,
        COUNT(DISTINCT tonnages.id_collecte) as NbTournees,
        SUM(tonnages.tonnage)/1000/ NULLIF(COUNT(*), 0) AS tonnage_moyen

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
    ) tonnages
    LEFT JOIN cflux ON tonnages.id_flux = cflux.id_flux
    GROUP BY 1, 2
    ORDER BY 1, 2
    """

    with connection.cursor() as cursor:
        cursor.execute(sql)
        rows = cursor.fetchall()
        cols = [col[0] for col in cursor.description]  # noms de colonnes

    data = [dict(zip(cols, row)) for row in rows]

    return JsonResponse(data, safe=False)
