"""
API Endpoint for sending emails via Mailjet.

This FastAPI application exposes a single POST endpoint at `/api/send_email`.  It
expects a JSON payload containing an `email` key.  The endpoint validates the
input, ensures that all required Mailjet configuration values are present, and
then uses the Mailjet API to send a notification email.  Errors are reported
with appropriate HTTP status codes and descriptive messages.

Deployment Notes
----------------
On Vercel, Python functions live inside the `api` directory.  The Vercel
runtime automatically detects a FastAPI application called `app` and serves
its routes.  Environment variables (`MAILJET_API_KEY`, `MAILJET_API_SECRET`,
`MAILJET_SENDER`, and `MAILJET_RECEIVER`) should be defined in the Vercel
dashboard.  If any are missing, the endpoint will return a 500 status
informing the caller of the misconfiguration.
"""

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
import os
import requests

# Instantiate the FastAPI application
app = FastAPI()

# Read Mailjet configuration from environment variables.  Using os.getenv
# prevents import‑time KeyError if a variable is missing.
MAILJET_API_KEY: str | None = os.getenv("MAILJET_API_KEY")
MAILJET_API_SECRET: str | None = os.getenv("MAILJET_API_SECRET")
MAILJET_SENDER: str | None = os.getenv("MAILJET_SENDER")
MAILJET_RECEIVER: str | None = os.getenv("MAILJET_RECEIVER")


@app.post("/api/send_email")
async def send_email(req: Request) -> JSONResponse:
    """Handle incoming requests to send a notification email via Mailjet."""
    data = await req.json()
    email = data.get("email")
    if not email:
        raise HTTPException(status_code=400, detail="Email manquant")

    # Ensure all Mailjet environment variables are available before sending
    if not all([MAILJET_API_KEY, MAILJET_API_SECRET, MAILJET_SENDER, MAILJET_RECEIVER]):
        raise HTTPException(
            status_code=500,
            detail=(
                "Configuration Mailjet manquante: veuillez définir "
                "MAILJET_API_KEY, MAILJET_API_SECRET, MAILJET_SENDER et MAILJET_RECEIVER."
            ),
        )

    payload = {
        "Messages": [
            {
                "From": {"Email": MAILJET_SENDER, "Name": "Spectra Media"},
                "To": [{"Email": MAILJET_RECEIVER, "Name": "Vincent"}],
                "Subject": "🎯 Nouveau contact landing page",
                "TextPart": f"Nouvel email curieux : {email}",
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
        raise HTTPException(status_code=500, detail=f"Erreur lors de la requête Mailjet : {exc}")

    if response.status_code == 200:
        return JSONResponse(content={"message": "Email envoyé via Mailjet"})
    raise HTTPException(status_code=500, detail=f"Mailjet : {response.text}")
