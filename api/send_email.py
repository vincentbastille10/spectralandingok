from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import smtplib
from email.message import EmailMessage
import os

app = FastAPI()

@app.post("/api/send_email")
async def send_email(request: Request):
    try:
        data = await request.json()
        user_email = data.get("email")
        if not user_email:
            return JSONResponse(status_code=400, content={"error": "Email manquant"})

        msg = EmailMessage()
        msg["Subject"] = "🎯 Nouveau contact landing page"
        msg["From"] = os.environ["EMAIL_FROM"]
        msg["To"] = os.environ["EMAIL_TO"]
        msg.set_content(f"Nouvel email curieux : {user_email}")

        with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
            smtp.starttls()
            smtp.login(os.environ["EMAIL_FROM"], os.environ["EMAIL_PASS"])
            smtp.send_message(msg)

        return {"message": "Email envoyé"}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
