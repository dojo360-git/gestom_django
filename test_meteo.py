# Commande pour executer ce script :
# python test_meteo.py

import json
import socket
import time
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


api_url = (
    "https://api.open-meteo.com/v1/forecast"
    "?latitude=48.626032&longitude=2.309739"
    "&current=temperature_2m,apparent_temperature,relative_humidity_2m,wind_speed_10m,weather_code,is_day"
    "&hourly=temperature_2m,precipitation,precipitation_probability,weather_code,wind_speed_10m"
    "&daily=temperature_2m_max,temperature_2m_min,sunrise,sunset"
    "&timezone=Europe/Paris"
)

fallback_api_url = "https://wttr.in/48.626032,2.309739?format=j1"


def fetch_json(url: str, max_attempts: int = 5) -> tuple[int, dict]:
    request = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Python test_meteo.py"
        },
    )

    retryable_http_codes = {502, 503, 504}
    last_error: Exception | None = None

    for attempt in range(1, max_attempts + 1):
        try:
            with urlopen(request, timeout=20) as response:
                status_code = response.getcode()
                body = response.read().decode("utf-8")
                data = json.loads(body)
            return status_code, data
        except HTTPError as err:
            last_error = err
            if err.code in retryable_http_codes and attempt < max_attempts:
                time.sleep(attempt * 2)
                continue
            raise
        except (URLError, socket.timeout, json.JSONDecodeError) as err:
            last_error = err
            if attempt < max_attempts:
                time.sleep(attempt)
                continue
            raise

    if last_error is not None:
        raise last_error
    raise RuntimeError("Erreur inconnue lors de l'appel API.")


def main() -> None:
    errors: list[str] = []
    sources = [
        ("Open-Meteo", api_url),
        ("wttr.in (fallback)", fallback_api_url),
    ]

    for source_name, source_url in sources:
        try:
            status_code, data = fetch_json(source_url)
            print(f"Source utilisee: {source_name}")
            print(f"Status HTTP: {status_code}")
            print("Reponse API :")
            print(json.dumps(data, indent=2, ensure_ascii=False))
            return
        except HTTPError as err:
            error_body = ""
            try:
                error_body = err.read().decode("utf-8", errors="replace")
            except Exception:
                error_body = "<impossible de lire le corps de la reponse>"

            msg = f"{source_name} -> Erreur HTTP: {err.code} - {err.reason}"
            if error_body:
                msg += f"\nCorps de la reponse: {error_body}"
            errors.append(msg)
        except URLError as err:
            errors.append(f"{source_name} -> Erreur reseau: {err.reason}")
        except socket.timeout:
            errors.append(f"{source_name} -> Timeout reseau")
        except json.JSONDecodeError:
            errors.append(f"{source_name} -> Reponse JSON invalide")

    print("Aucune API meteo n'a repondu correctement.")
    print("Details des erreurs :")
    for item in errors:
        print(f"- {item}")
    print(
        "Diagnostic: verifie le VPN/proxy/firewall Windows ou entreprise. "
        "Ce type d'erreur indique souvent un blocage reseau externe."
    )


if __name__ == "__main__":
    main()






# reponse api_url_ api.open-meteo
# {"latitude":48.64,"longitude":2.3199997,"generationtime_ms":0.1901388168334961,"utc_offset_seconds":7200,"timezone":"Europe/Paris","timezone_abbreviation":"GMT+2","elevation":69.0,"current_units":{"time":"iso8601","interval":"seconds","temperature_2m":"°C","relative_humidity_2m":"%","precipitation":"mm","wind_speed_10m":"km/h","weather_code":"wmo code"},"current":{"time":"2026-04-04T18:45","interval":900,"temperature_2m":18.1,"relative_humidity_2m":57,"precipitation":0.00,"wind_speed_10m":12.8,"weather_code":0},"hourly_units":{"time":"iso8601","temperature_2m":"°C","precipitation":"mm"},"hourly":{"time":["2026-04-04T00:00","2026-04-04T01:00","2026-04-04T02:00","2026-04-04T03:00","2026-04-04T04:00","2026-04-04T05:00","2026-04-04T06:00","2026-04-04T07:00","2026-04-04T08:00","2026-04-04T09:00","2026-04-04T10:00","2026-04-04T11:00","2026-04-04T12:00","2026-04-04T13:00","2026-04-04T14:00","2026-04-04T15:00","2026-04-04T16:00","2026-04-04T17:00","2026-04-04T18:00","2026-04-04T19:00","2026-04-04T20:00","2026-04-04T21:00","2026-04-04T22:00","2026-04-04T23:00","2026-04-05T00:00","2026-04-05T01:00","2026-04-05T02:00","2026-04-05T03:00","2026-04-05T04:00","2026-04-05T05:00","2026-04-05T06:00","2026-04-05T07:00","2026-04-05T08:00","2026-04-05T09:00","2026-04-05T10:00","2026-04-05T11:00","2026-04-05T12:00","2026-04-05T13:00","2026-04-05T14:00","2026-04-05T15:00","2026-04-05T16:00","2026-04-05T17:00","2026-04-05T18:00","2026-04-05T19:00","2026-04-05T20:00","2026-04-05T21:00","2026-04-05T22:00","2026-04-05T23:00","2026-04-06T00:00","2026-04-06T01:00","2026-04-06T02:00","2026-04-06T03:00","2026-04-06T04:00","2026-04-06T05:00","2026-04-06T06:00","2026-04-06T07:00","2026-04-06T08:00","2026-04-06T09:00","2026-04-06T10:00","2026-04-06T11:00","2026-04-06T12:00","2026-04-06T13:00","2026-04-06T14:00","2026-04-06T15:00","2026-04-06T16:00","2026-04-06T17:00","2026-04-06T18:00","2026-04-06T19:00","2026-04-06T20:00","2026-04-06T21:00","2026-04-06T22:00","2026-04-06T23:00","2026-04-07T00:00","2026-04-07T01:00","2026-04-07T02:00","2026-04-07T03:00","2026-04-07T04:00","2026-04-07T05:00","2026-04-07T06:00","2026-04-07T07:00","2026-04-07T08:00","2026-04-07T09:00","2026-04-07T10:00","2026-04-07T11:00","2026-04-07T12:00","2026-04-07T13:00","2026-04-07T14:00","2026-04-07T15:00","2026-04-07T16:00","2026-04-07T17:00","2026-04-07T18:00","2026-04-07T19:00","2026-04-07T20:00","2026-04-07T21:00","2026-04-07T22:00","2026-04-07T23:00","2026-04-08T00:00","2026-04-08T01:00","2026-04-08T02:00","2026-04-08T03:00","2026-04-08T04:00","2026-04-08T05:00","2026-04-08T06:00","2026-04-08T07:00","2026-04-08T08:00","2026-04-08T09:00","2026-04-08T10:00","2026-04-08T11:00","2026-04-08T12:00","2026-04-08T13:00","2026-04-08T14:00","2026-04-08T15:00","2026-04-08T16:00","2026-04-08T17:00","2026-04-08T18:00","2026-04-08T19:00","2026-04-08T20:00","2026-04-08T21:00","2026-04-08T22:00","2026-04-08T23:00","2026-04-09T00:00","2026-04-09T01:00","2026-04-09T02:00","2026-04-09T03:00","2026-04-09T04:00","2026-04-09T05:00","2026-04-09T06:00","2026-04-09T07:00","2026-04-09T08:00","2026-04-09T09:00","2026-04-09T10:00","2026-04-09T11:00","2026-04-09T12:00","2026-04-09T13:00","2026-04-09T14:00","2026-04-09T15:00","2026-04-09T16:00","2026-04-09T17:00","2026-04-09T18:00","2026-04-09T19:00","2026-04-09T20:00","2026-04-09T21:00","2026-04-09T22:00","2026-04-09T23:00","2026-04-10T00:00","2026-04-10T01:00","2026-04-10T02:00","2026-04-10T03:00","2026-04-10T04:00","2026-04-10T05:00","2026-04-10T06:00","2026-04-10T07:00","2026-04-10T08:00","2026-04-10T09:00","2026-04-10T10:00","2026-04-10T11:00","2026-04-10T12:00","2026-04-10T13:00","2026-04-10T14:00","2026-04-10T15:00","2026-04-10T16:00","2026-04-10T17:00","2026-04-10T18:00","2026-04-10T19:00","2026-04-10T20:00","2026-04-10T21:00","2026-04-10T22:00","2026-04-10T23:00"],"temperature_2m":[11.8,12.2,12.1,12.1,12.1,12.1,12.1,12.0,11.8,12.0,12.5,13.4,14.1,15.6,15.3,15.9,17.1,18.3,18.5,18.0,16.8,15.0,13.7,13.0,12.6,12.5,12.0,11.6,10.9,10.3,10.3,9.9,9.6,10.2,11.5,12.9,13.6,14.2,15.3,15.3,15.3,14.8,14.2,13.8,12.8,11.4,10.1,9.1,8.1,7.3,6.6,6.2,5.8,5.6,4.2,4.1,4.4,5.5,7.4,9.5,11.4,13.0,14.3,15.3,15.9,16.2,16.0,15.3,13.8,12.0,10.9,9.9,9.1,8.3,7.7,7.3,7.0,6.6,6.4,6.2,6.4,8.2,10.4,13.0,15.6,17.9,19.8,20.9,21.7,21.9,21.5,20.4,18.5,17.0,15.4,13.9,12.9,12.1,11.4,10.7,10.1,9.6,9.0,8.5,8.7,10.0,12.1,14.2,16.4,18.7,20.4,21.6,22.2,22.3,21.7,20.4,19.1,17.7,16.3,15.0,14.0,13.2,12.4,11.5,10.7,10.0,9.3,8.8,9.1,11.1,13.9,16.2,17.5,18.4,18.9,18.7,18.2,17.4,16.2,14.7,13.1,11.6,10.1,8.9,8.2,7.8,7.4,7.0,6.6,6.3,5.9,5.5,5.7,7.0,8.8,10.6,12.2,13.7,15.0,16.0,16.7,16.9,16.4,15.5,14.4,13.2,11.7,10.6],"precipitation":[0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00,0.00]}}