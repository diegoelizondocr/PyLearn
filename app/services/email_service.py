import requests
import resend
from loguru import logger
from fastapi import HTTPException
from app.config import settings
from app.models.schemas import EmailRequest


class EmailService:

    def send_email_new(self, email_data: EmailRequest) -> dict:
        logger.info(f"Enviando correo a: {email_data.to}")

        if not settings.resend_api_key:
            raise HTTPException(status_code=503, detail="Servicio de correo no configurado")

        resend.api_key = settings.resend_api_key
        result = resend.Emails.send({
            "from": settings.resend_from_email,
            "to": [str(email_data.to)],
            "subject": email_data.subject,
            "html": email_data.html
        })

        logger.success(f"Correo enviado correctamente a {email_data.to}")
        return {
            "message": "Correo enviado exitosamente",
            "data": result
        }

    def send_email(self, email_data: EmailRequest) -> dict:
        logger.info(f"Enviando correo a: {email_data.to}")

        if not settings.resend_api_key:
            raise HTTPException(status_code=503, detail="Servicio de correo no configurado")

        url = "https://api.resend.com/emails"
        headers = {
            "Authorization": f"Bearer {settings.resend_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "from": settings.resend_from_email,
            "to": [email_data.to],
            "subject": email_data.subject,
            "html": email_data.html
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            
            if response.status_code == 200:
                logger.success(f"Correo enviado correctamente a {email_data.to}")
                return {
                    "message": "Correo enviado exitosamente",
                    "data": response.json()
                }
            else:
                logger.error(f"Error de Resend: {response.status_code} - {response.text}")
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Error al enviar correo: {response.text}"
                )
        except requests.exceptions.RequestException as e:
            logger.error(f"Error de conexión con Resend: {e}")
            raise HTTPException(status_code=503, detail="No se pudo conectar con el servicio de correo")