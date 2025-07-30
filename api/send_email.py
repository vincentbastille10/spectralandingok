import os
import smtplib
from email.message import EmailMessage

# Récupère les paramètres depuis les variables d’environnement
GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASS = os.getenv("GMAIL_PASS")
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL", "spectramediabots@gmail.com")

def handler(request, response):
    try:
        # Récupère l’adresse saisie par l’utilisateur dans le JSON
        body = request.get_json()
        user_email = body.get('email')
        if not user_email:
            response.status_code = 400
       	    return response.json({ "error": "Email manquant" })

        # Prépare le message
        msg = EmailMessage()
        msg['Subject'] = '🎯 Nouveau contact landing page'
        msg['From'] = GMAIL_USER
        msg['To'] = RECEIVER_EMAIL
        msg.set_content(f"Nouvel email curieux : {user_email}")

        # Envoie via Gmail en SMTP
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(GMAIL_USER, GMAIL_PASS)
            smtp.send_message(msg)

        response.status_code = 200
        return response.json({ "message": "Email envoyé" })

    except Exception as e:
        response.status_code = 500
        return response.json({ "error": str(e) })
