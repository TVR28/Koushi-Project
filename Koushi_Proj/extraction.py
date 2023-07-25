#Uploading PDF , extracting text and translating it and generating audio

import pyttsx3
import PyPDF2
import unidecode
from gtts import gTTS
from googletrans import Translator

#uploading pdf and accepting it
book = open('lec1.pdf','rb')
reader = PyPDF2.PdfReader(book)
pages = len(reader.pages)
print("No.of Pages: ",pages)
i=1
converted_en=[]
converted_te =[]
for i in range(pages):
    page = reader.pages[i]
    text = page.extract_text()
    text = "".join(text.splitlines())
    cleaned_text = unidecode.unidecode(text)

    translater = Translator()
    converted_en.append(translater.translate(cleaned_text, dest="en").text)
    translater = Translator()
    converted_te.append(translater.translate(cleaned_text, dest="te").text)

    audio = gTTS(text=converted_en[i], lang='en')
    audio.save(f"page{i+1}_en.mp3")

    audio = gTTS(text=converted_te[i], lang='te')
    audio.save(f"page{i+1}_te.mp3")

print("Succesful")

