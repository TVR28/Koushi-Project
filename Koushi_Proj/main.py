#Importing required libraries 
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


st.set_page_config(page_title="Koushi App",layout = 'wide')


st.markdown("<h1 style='text-align:center; padding:10px; font-size:80px; color:#FF4B4B'>ReedIT</h1>",unsafe_allow_html=True)
st.markdown("---")

st.markdown("<h1 style='text-align:left; font-size:50px; color:#FF4B4B'>Upload a PDF</h1>",unsafe_allow_html=True)


if "once" not in st.session_state:
    st.session_state.once = True
if "conv" not in st.session_state:
    st.session_state.conv = True
if "count" not in st.session_state:
    st.session_state.count = 1

# All the preprocesses (processing pdf,image conversion etc)

i=1
converted_en=[]
converted_te=[]
pages = 1

file = st.file_uploader("Upload a PDF", type="pdf")
st.markdown("---")
if file is not None:
    fname = (file.name).split('.')[0]
    reader = PyPDF2.PdfReader(file) 
    pages = len(reader.pages)
    st.markdown(f"<h1 style='text-align:left; padding:5px;font-style:italic; font-size:20px; color:#FF4B4B'>No.of Pages: {pages}</h1>",unsafe_allow_html=True)
    for i in range(0,pages): #Runs for no.of pages
        page = reader.pages[i]
        text = page.extract_text()
        text = "".join(text.splitlines())
        cleaned_text = unidecode.unidecode(text)
        translater = Translator()
        converted_en.append(translater.translate(cleaned_text, dest="en").text) #adding each page en text 
        translater = Translator()
        converted_te.append(translater.translate(cleaned_text, dest="te").text) #adding each page te text
        if st.session_state.once == True:      
            audio = gTTS(text=converted_en[i], lang='en')
            audio.save(f"{fname}_page{i+1}_EN.mp3")
            audio = gTTS(text=converted_te[i], lang='te')
            audio.save(f"{fname}_page{i+1}_TE.mp3")
    st.session_state.once = False

    i = 1
    #convert pdf to images ---->  Place inside a button
    if st.session_state.conv == True: #Only happens once
        pages = convert_from_path(file.name, 500,poppler_path=r'C:\Program Files\poppler-23.07.0\Library\bin')
        for page in pages:
            page.save(f'{fname}_page{i}.jpg', 'JPEG')
            i+=1
        st.session_state.conv = False
    i=1

    if st.session_state.count >= 1:
        st.image(f'{fname}_page{st.session_state.count}.jpg', caption=f'Page{st.session_state.count}',width = 500)
        audio_file_en = open(f'{fname}_page{st.session_state.count}_en.mp3', 'rb')
        audio_bytes_en = audio_file_en.read()
        audio_file_te = open(f'{fname}_page{st.session_state.count}_te.mp3', 'rb')
        audio_bytes_te = audio_file_te.read()
        if st.button("Next",type='primary'):
            st.session_state.count +=1
            if st.session_state.count > pages:
                st.session_state.count=pages
                st.success("End of pages")
                time.sleep(1)
                st.experimental_rerun()
            else:
                st.experimental_rerun()
        if st.button("Prev",type='primary'):
            st.session_state.count -=1
            if st.session_state.count <1:
                st.session_state.count = 1
                st.info("This is the First Page")
                time.sleep(1)
                st.experimental_rerun()
            else:
                st.experimental_rerun()
        st.markdown('---')
        # with st.expander("English Audio"):
        with st.expander("**English Text**"):
            st.header(converted_en[st.session_state.count - 1])
        st.markdown("<h1 style='text-align:left; padding:5px;font-style:italic; font-size:20px; color:#FF4B4B'>English Audio:</h1>",unsafe_allow_html=True)
        st.audio(audio_bytes_en, format='audio/mp3')

        st.markdown('---')
        # with st.expander("Telugu Audio"):
        with st.expander("**Telugu Text**"):
            st.header(converted_te[st.session_state.count - 1])
        st.markdown("<h1 style='text-align:left; padding:5px;font-style:italic; font-size:20px; color:#FF4B4B'>Telugu Audio:</h1>",unsafe_allow_html=True)
        st.audio(audio_bytes_te, format='audio/mp3')



