from fastapi import FastAPI, Request, Form
from dotenv import load_dotenv
import openai
import os
from confluence import search_confluence
from twilio.rest import Client
import logging

print("🚀 Завантажено main.py")

# Логування
logging.basicConfig(level=logging.INFO)

# Завантаження змінних оточення
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Перевірка змінних
logging.info("✅ ENV VARIABLES:")
for k, v in os.environ.items():
    if "CONFLUENCE" in k or "TWILIO" in k or "OPENAI" in k:
        logging.info(f"{k} = {v}")

app = FastAPI()

@app.post("/webhook")
async def whatsapp_webhook(
    request: Request,
    Body: str = Form(...),
    From: str = Form(...)
):
    try:
        logging.info(f"💬 Запит від {From}: {Body}")
        query = Body
        pages = search_confluence(query)

        summary = "\n\n".join(
            [f"*{p['title']}*\n{p['link']}" for p in pages]
        ) or "Нічого не знайдено."

        message = f"Ось, що я знайшов:\n\n{summary}"
        send_whatsapp_reply(to=From, body=message)
        return {"status": "ok"}

    except Exception as e:
        logging.error(f"❌ Помилка у webhook: {str(e)}")
        return {"status": "error", "message": str(e)}

def send_whatsapp_reply(to: str, body: str):
    logging.info(f"📤 Відправляю повідомлення до {to}")
    client = Client(
        os.getenv("TWILIO_ACCOUNT_SID"),
        os.getenv("TWILIO_AUTH_TOKEN")
    )
    client.messages.create(
        from_=os.getenv("TWILIO_WHATSAPP_NUMBER"),
        to=to,
        body=body
    )
