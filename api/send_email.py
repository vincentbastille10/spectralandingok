import os
import requests
from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI()

MAILJET_API_KEY = os.getenv("MAILJET_API_KEY")
MAILJET_API_SECRET = os.getenv("MAILJET_API_SECRET")
MAILJET_SENDER = os.getenv("MAILJET_SENDER")
MAILJET_RECEIVER = os.getenv("MAILJET_RECEIVER")

@app.post("/api/send_email")
async def send_email(req: Request) -> JSONResponse:
    data = await req.json()
    email = data.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Email manquant")

    if not all([MAILJET_API_KEY, MAILJET_API_SECRET, MAILJET_SENDER, MAILJET_RECEIVER]):
        raise HTTPException(
            status_code=500,
            detail="Configuration Mailjet manquante: veuillez définir MAILJET_API_KEY, MAILJET_API_SECRET, MAILJET_SENDER et MAILJET_RECEIVER."
        )

    payload = {
        "Messages": [
            {
                "From": {"Email": MAILJET_SENDER, "Name": "Spectra Media"},
                "To": [{"Email": MAILJET_RECEIVER, "Name": "Vincent"}],
                "Subject": "🎯 Nouveau contact landing page",
                "TextPart": f"Nouvel email curieux : {email}",
            }
        ]
    }

    try:
        response = requests.post(
            "https://api.mailjet.com/v3.1/send",
            auth=(MAILJET_API_KEY, MAILJET_API_SECRET),
            json=payload,
            timeout=10,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erreur Mailjet : {exc}")

    if response.status_code == 200:
        return JSONResponse(content={"message": "Email envoyé via Mailjet"})
    raise HTTPException(status_code=500, detail=f"Mailjet : {response.text}")
