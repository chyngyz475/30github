from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route("/whatsapp", methods=["POST"])
def whatsapp_reply():
    msg = request.form.get("Body")  # Получаем сообщение пользователя
    resp = MessagingResponse()
    resp.message(f"Ты написал: {msg}")  # Ответ на сообщение
    return str(resp)

if __name__ == "__main__":
    app.run(port=5000)
