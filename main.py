import smtplib
from email.message import EmailMessage
import json

def handler(request, response):
    try:
        body = request.get_json()
        user_email = body.get('email')

        msg = EmailMessage()
        msg['Subject'] = '🎯 Nouveau contact landing page'
        msg['From'] = 'vinylestorefrance@gmail.com'
        msg['To'] = 'spectramediabots@gmail.com'
        msg.set_content(f"Nouvel email curieux : {user_email}")

        smtp = smtplib.SMTP('smtp.gmail.com', 587)
        smtp.starttls()
        smtp.login("vinylestorefrance@gmail.com", "TON_MDP_APP")  # utilise un mot de passe d'application Gmail
        smtp.send_message(msg)
        smtp.quit()

        response.status_code = 200
        return response.json({ "message": "Email envoyé" })
    
    except Exception as e:
        response.status_code = 500
        return response.json({ "error": str(e) })
