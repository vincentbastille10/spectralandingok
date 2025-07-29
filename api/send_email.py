from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import os, requests

app = FastAPI()

MAILJET_API_KEY    = os.environ["MAILJET_API_KEY"]
MAILJET_API_SECRET = os.environ["MAILJET_API_SECRET"]
MAILJET_SENDER     = os.environ["MAILJET_SENDER"]      # vinylestorefrance@gmail.com
MAILJET_RECEIVER   = os.environ["MAILJET_RECEIVER"]    # vinylestorefrance@gmail.com

@app.post("/api/send_email")
async def send_email(req: Request):
    data  = await req.json()
    email = data.get("email")
    if not email:
        return JSONResponse(status_code=400, content={"error": "Email manquant"})

    payload = {
        "Messages": [{
            "From": {"Email": MAILJET_SENDER, "Name": "Spectra Media"},
            "To":   [{"Email": MAILJET_RECEIVER, "Name": "Vincent"}],
            "Subject": "🎯 Nouveau contact landing page",
            "TextPart": f"Nouvel email curieux : {email}"
        }]
    }

    r = requests.post(
        "https://api.mailjet.com/v3.1/send",
        auth=(MAILJET_API_KEY, MAILJET_API_SECRET),
        json=payload
    )

    if r.status_code == 200:
        return {"message": "Email envoyé via Mailjet"}
    return JSONResponse(status_code=500, content={"error": f"Mailjet: {r.text}"})
