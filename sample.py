import streamlit as st
import time
from PIL import Image
import PyPDF2
import unidecode
from pdf2image import convert_from_path
from gtts import gTTS
from googletrans import Translator
import os
from io import BytesIO

from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/drive']
SERVICE_ACCOUNT_FILE = 'service_account.json'
PARENT_FOLDER_ID = "1xbz6eR3dcs7wK4R7Suapz8hYMx8X3SV6" #id at the end of url when opened the drive folder


def authenticate():
    creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes = SCOPES)
    return creds

def upload_files(file_path):
    creds = authenticate()
    service = build('drive','v3',credentials=creds)

    file_metadata = {
        'name' : ['English.mp3','Telugu.mp3'],
        'parents' : [PARENT_FOLDER_ID]
    }

    file = service.files().create(
        body = file_metadata,
        media_body = file_path
    ).execute()



i=1
converted_en=""
converted_te=""
pages = 1

# st.set_page_config(page_title="Koushi App")
# st.title("Testing App")

sample_text = """Contrary to popular belief, Lorem Ipsum is not simply random text. It has roots in a piece of classical Latin literature from 45 BC, making it over 2000 years old. Richard McClintock, a Latin professor at Hampden-Sydney College in Virginia, looked up one of the more obscure Latin words, consectetur, from a Lorem Ipsum passage, and going through the cites of the word in classical literature, discovered the undoubtable source. Lorem Ipsum comes from sections 1.10.32 and 1.10.33 of "de Finibus Bonorum et Malorum" (The Extremes of Good and Evil) by Cicero, written in 45 BC. This book is a treatise on the theory of ethics, very popular during the Renaissance."""
# text = "".join(sample_text.splitlines())
cleaned_text = unidecode.unidecode(sample_text)
translater = Translator()
converted_en = translater.translate(cleaned_text, dest="en").text #adding each page en text 
translater = Translator()
converted_te = translater.translate(cleaned_text, dest="te").text #adding each page te text


audio = gTTS(text=converted_en, lang='en')
audio.save("english.mp3")
upload_files("english.mp3")
# audio.save(f"english.mp3")

audiot = gTTS(text=converted_te, lang='te')
audiot.save(f"telugu.mp3")
upload_files("telugu.mp3")
