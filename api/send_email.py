from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import os
import requests

@app.post("/")
async def send_email(request: Request):
    try:
        data = await request.json()
        user_email = data.get("email")
        if not user_email:
            return JSONResponse(status_code=400, content={"error": "Email manquant"})

        mail_data = {
            "Messages": [
                {
                    "From": {
                        "Email": MAILJET_SENDER,
                        "Name": "Spectra Media"
                    },
                    "To": [
                        {
                            "Email": MAILJET_RECEIVER,
                            "Name": "Vincent"
                        }
                    ],
                    "Subject": "🎯 Nouveau contact landing page",
                    "TextPart": f"Nouvel email curieux : {user_email}"
                }
            ]
        }

        resp = requests.post(
            "https://api.mailjet.com/v3.1/send",
            auth=(MAILJET_API_KEY, MAILJET_API_SECRET),
            json=mail_data
        )

        if resp.status_code == 200:
            return {"message": "Email envoyé via Mailjet"}
        else:
            # Retourne le code et le texte complet pour debug
            return JSONResponse(
                status_code=resp.status_code,
                content={"error": f"Mailjet error: {resp.text}"}
            )

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
