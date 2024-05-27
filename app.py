from flask import Flask, request, jsonify, make_response
from openai import OpenAI
from heyoo import WhatsApp
from pydub import AudioSegment
from dotenv import load_dotenv
import os
import requests
import io

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
app = Flask(__name__)

def send_message(meta_token, phone_number_id, phone, text):
    messenger = WhatsApp(meta_token,phone_number_id=phone_number_id)
    messenger.send_message(text,phone)

def verify_token():
    hub_token = os.getenv("HUB_TOKEN")
    if request.args.get('hub.verify_token') == hub_token:
        return request.args.get('hub.challenge')
    return "Auth error"

def get_audio_transcription(audio_id, meta_token):
    try:
        audio_info = requests.get(
            f"https://graph.facebook.com/v19.0/{audio_id}", 
            headers={"Authorization": f"Bearer {meta_token}"}
        ).json()
        audio_url = audio_info['url']
        audio_content = requests.get(audio_url, headers={"Authorization": f"Bearer {meta_token}"})
        audio_stream = io.BytesIO(audio_content.content)
        AudioSegment.from_file(audio_stream).export("audio.mp3", format='mp3')
        with open("audio.mp3", "rb") as audio_file:
            transcription = OpenAI().audio.transcriptions.create(model="whisper-1", file=audio_file)
        return transcription.text
    except Exception as e:
        print(e)
        return None

@app.route('/gpt_webhook_consult', methods=['GET', 'POST'])
def gpt_webhook_consult():
    meta_token = os.getenv("META_TOKEN")
    phone_number_id = os.getenv("PHONE_NUMBER_ID")
    gpt_model = os.getenv("GPT_MODEL")

    if request.method == "GET":
        return verify_token()

    data = request.get_json()
    changes = data.get('entry', [])[0].get('changes', [])[0].get('value', {})
    if 'messages' not in changes:
        return make_response(jsonify({"message": "Not a message"}), 200)

    message = changes['messages'][0]
    phone_number = message['from']
    main_content = "You are a whatsapp chat to handle simple requests. No matter the language of the question, you will respond in English."
    response = None

    if message['type'] == 'text':
        user_text = message['text']['body']
        response = client.chat.completions.create(
            model=gpt_model,
            messages=[
                {"role": "system", "content": main_content},
                {"role": "user", "content": user_text}
            ]
        )
    elif message['type'] == 'audio':
        transcription = get_audio_transcription(message['audio']['id'], meta_token)
        if transcription:
            response = client.chat.completions.create(
                model=gpt_model,
                messages=[
                    {"role": "system", "content": main_content},
                    {"role": "user", "content": transcription}
                ]
            )
        else:
            send_message(meta_token, phone_number_id, phone_number, 'Error processing audio')
            return make_response(jsonify({"message": "Error processing audio"}), 200)
    else:
        response = client.chat.completions.create(
            model=gpt_model,
            messages=[
                {"role": "user", "content": "Give me a short message mentioning there was an error and invite to try again later"}
            ]
        )

    if response:
        message_content = response.choices[0].message['content']
        if send_message(meta_token, phone_number_id, phone_number, message_content):
            return make_response(jsonify({"message": "Success"}), 200)

    return make_response(jsonify({"message": "Failed to send message"}), 200)

if __name__ == '__main__':
    app.run(debug=True)
