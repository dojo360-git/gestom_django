import csv
import re
from datetime import datetime
from io import StringIO

from django.db import connection
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET

from .models import CollectPrev


def _empty_text_response():
    return HttpResponse("", content_type="text/plain; charset=utf-8")


def _classement_sort_key(item):
    raw = (getattr(item, "classement", "") or "").strip()
    match = re.search(r"\d+", raw)
    if match:
        return (0, int(match.group(0)), raw.lower())
    return (1, raw.lower(), item.pk)


def _agent_nom(agent):
    return agent.nom if agent else ""


def _format_time(value):
    return value.strftime("%H:%M") if value else ""


@require_GET
def prevision(request):
    if request.GET.get("pw") != "regiecdea":
        return _empty_text_response()

    raw_date = request.GET.get("date")
    try:
        selected_date = datetime.strptime(raw_date or "", "%Y-%m-%d").date()
    except ValueError:
        return _empty_text_response()

    rows = list(
        CollectPrev.objects.select_related(
            "itineraire",
            "vehicule",
            "flux",
            "agent_1",
            "agent_2",
            "agent_3",
        ).filter(date=selected_date)
    )

    output = StringIO()
    writer = csv.writer(output, delimiter="\t", lineterminator="\n")
    writer.writerow(["date", "itineraire", "vehicule", "flux", "agent1", "agent2", "agent3", "depart", "infos"])
    for item in sorted(rows, key=_classement_sort_key):
        writer.writerow(
            [
                item.date.strftime("%d/%m/%Y") if item.date else "",
                str(item.itineraire) if item.itineraire else "",
                str(item.vehicule) if item.vehicule else "",
                str(item.flux) if item.flux else "",
                _agent_nom(item.agent_1),
                _agent_nom(item.agent_2),
                _agent_nom(item.agent_3),
                _format_time(item.depart),
                item.infos or "",
            ]
        )

    return HttpResponse(output.getvalue(), content_type="text/tab-separated-values; charset=utf-8")


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
