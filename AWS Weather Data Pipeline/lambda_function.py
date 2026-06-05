import json
import boto3
import urllib.request
from datetime import datetime, timezone

# ── config ──────────────────────────────────────────────
S3_BUCKET      = "weather-pipeline-vivek"   # ← change
CITIES         = ["Mumbai", "Delhi", "Bangalore", "Chennai"]
UNITS          = "metric"
SSM_KEY        = "/weather-pipeline/api-key"
SENDER_EMAIL   = "email@gmail.com"               # ← change
RECEIVER_EMAIL = "email@gmail.com"               # ← change
# ────────────────────────────────────────────────────────

ssm = boto3.client("ssm",  region_name="us-east-1")
s3  = boto3.client("s3",   region_name="us-east-1")
ses = boto3.client("ses",  region_name="us-east-1")


def get_api_key():
    resp = ssm.get_parameter(Name=SSM_KEY, WithDecryption=True)
    return resp["Parameter"]["Value"]


def fetch_weather(city: str, api_key: str) -> dict:
    url = (
        f"https://api.openweathermap.org/data/2.5/weather"
        f"?q={city}&appid={api_key}&units={UNITS}"
    )
    with urllib.request.urlopen(url, timeout=10) as resp:
        raw = json.loads(resp.read().decode())

    return {
        "city":        city,
        "timestamp":   datetime.now(timezone.utc).isoformat(),
        "temperature": raw["main"]["temp"],
        "feels_like":  raw["main"]["feels_like"],
        "humidity":    raw["main"]["humidity"],
        "pressure":    raw["main"]["pressure"],
        "weather":     raw["weather"][0]["description"],
        "wind_speed":  raw["wind"]["speed"],
        "visibility":  raw.get("visibility", None),
        "raw":         raw
    }


def build_s3_key(city: str, now: datetime) -> str:
    return (
        f"weather/{city.lower()}/"
        f"{now.year}/{now.month:02d}/{now.day:02d}/"
        f"{now.hour:02d}-{now.minute:02d}.json"
    )


def send_summary_email(results: list, timestamp: str):
    lines = []
    for r in results:
        if r["status"] == "ok":
            lines.append(
                f"📍 {r['city']}\n"
                f"   🌡 Temp     : {r['temperature']}°C (feels {r['feels_like']}°C)\n"
                f"   💧 Humidity : {r['humidity']}%\n"
                f"   🌬 Wind     : {r['wind_speed']} m/s\n"
                f"   ☁  Weather  : {r['weather']}\n"
            )
        else:
            lines.append(f"📍 {r['city']} — fetch failed: {r.get('error','unknown')}\n")

    body = f"Weather Report — {timestamp}\n\n" + "\n".join(lines)

    ses.send_email(
        Source=SENDER_EMAIL,
        Destination={"ToAddresses": [RECEIVER_EMAIL]},
        Message={
            "Subject": {"Data": f"🌤 Weather Update — {timestamp}"},
            "Body":    {"Text": {"Data": body}}
        }
    )
    print(f"✓ Email sent to {RECEIVER_EMAIL}")


def lambda_handler(event, context):
    api_key = get_api_key()
    now     = datetime.now(timezone.utc)
    results = []

    for city in CITIES:
        try:
            data   = fetch_weather(city, api_key)
            s3_key = build_s3_key(city, now)

            s3.put_object(
                Bucket      = S3_BUCKET,
                Key         = s3_key,
                Body        = json.dumps(data, indent=2),
                ContentType = "application/json"
            )

            print(f"✓ {city}: {data['temperature']}°C | saved → {s3_key}")

            results.append({
                "city":        city,
                "status":      "ok",
                "key":         s3_key,
                "temperature": data["temperature"],
                "feels_like":  data["feels_like"],
                "humidity":    data["humidity"],
                "wind_speed":  data["wind_speed"],
                "weather":     data["weather"]
            })

        except Exception as e:
            print(f"✗ {city}: ERROR — {e}")
            results.append({
                "city":   city,
                "status": "error",
                "error":  str(e)
            })

    # send summary email after all cities fetched
    try:
        send_summary_email(results, now.strftime("%Y-%m-%d %H:%M UTC"))
    except Exception as e:
        print(f"✗ Email failed: {e}")

    return {
        "statusCode": 200,
        "timestamp":  now.isoformat(),
        "results":    results
    }
