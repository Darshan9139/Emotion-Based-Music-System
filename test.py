import imghdr
from logging import PlaceHolder
from re import A
from streamlit_webrtc import webrtc_streamer,RTCConfiguration
from streamlit_player import st_player
import streamlit.components.v1 as components
from streamlit_gallery.utils.readme import readme
from ImageEmotionDetection import FacialExpressionModel
import streamlit as st
import av
import cv2
import numpy as np
import os,time
import random

SONGS_DIR='Songs/'
ONLINE_PATH_DIR='Links/'
pred=''
facec = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
model = FacialExpressionModel("model.json", "model_weights.h5")
font = cv2.FONT_HERSHEY_SIMPLEX
EMOTIONS_LIST = ["Angry", "Disgust",
                    "Fear", "Happy",
                    "Neutral", "Sad",
                    "Surprise"]
class emotion:
    emotion=''
    def get_emotion(self):
        return self.emotion
    def set_emotion(self,emotion):
        self.emotion=emotion

mood=emotion()

st.set_page_config(layout="wide")

def video_frame_callback(frame):
    global pred
    fr = frame.to_ndarray(format="bgr24")
    #print(type(img))
    gray_fr = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
    faces = facec.detectMultiScale(gray_fr, 1.3, 5)
    for (x, y, w, h) in faces:
        fc = gray_fr[y:y+h, x:x+w]
        roi = cv2.resize(fc, (48, 48))
        pred = model.predict_emotion(roi[np.newaxis, :, :, np.newaxis])
        mood.set_emotion(pred)
        #print(pred)
        cv2.putText(fr, pred, (x, y), font, 1, (255, 255, 0), 2)
        cv2.rectangle(fr,(x,y),(x+w,y+h),(255,0,0),2)

    return av.VideoFrame.from_ndarray(fr, format="bgr24")

st.sidebar.header('Menu')
module_name = st.sidebar.selectbox(
    'Select Module',
    ('Photo', 'Video', 'Emotioan Based Music system','Songs Manager')
)
if module_name=='Photo':
    img_file_buffer = st.camera_input("Take a picture")
    st.title('OR')
    uploaded_file = st.file_uploader("Choose a file")

    if img_file_buffer is not None:
        # To read image file buffer as bytes:
        bytes_data = img_file_buffer.getvalue()
        # Check the type of bytes_data:
        # Should output: <class 'bytes'>
        st.write(type(bytes_data))
    if uploaded_file is not None:
        # To read file as bytes:
        bytes_data = uploaded_file.getvalue()
        st.write(bytes_data)


elif module_name=='Video':
    webrtc_streamer(key="example", video_frame_callback=video_frame_callback)
    st.header('Your Mood:')
    emotion = np.load("emotion.npy")[0]



elif module_name=='Emotioan Based Music system':
    c1, c2  = st.columns([4, 4])
    with c1:
        webrtc_streamer(key="example", video_frame_callback=video_frame_callback)
        play = st.button("▶️ Play Song Based On Mood")
        if(play):
            with c2:
                mood_name='Angry'
                with open(ONLINE_PATH_DIR+mood_name+'/LINKS.txt', "r") as links:
                    url = links.readlines()
                    st.subheader('Playlist:')
                    if(len(url)!=0):
                        components.html("""
                        <iframe src='"""+url[0]+"""?utm_source=generator' width="100%" height="380" frameBorder="0" allowtransparency="true" allow="encrypted-media"></iframe>""",height=300,scrolling=True)
                    else:
                        st.warning("Please add playlist link")


                

else:
    st.header("Spotify Playlist")
    mood_name=st.selectbox('Select Mood',EMOTIONS_LIST)
    link=st.text_input("Paste Link Here",value='')
    link=link.replace('https://open.spotify.com/','https://open.spotify.com/embed/',1)
    path=ONLINE_PATH_DIR+mood_name
    if not os.path.exists(path): 
            os.makedirs(path)
    with open(os.path.join(path,'LINKS.txt'),"w") as f: 
            f.write(link)

    with open(os.path.join(path,'LINKS.txt'),"w") as f: 
            f.write(link)
    with open(ONLINE_PATH_DIR+mood_name+'/LINKS.txt', "r") as links:
                    url = links.readlines()
    st.subheader('Playlist:')
    if(len(url)!=0):
        components.html("""
        <iframe src='"""+url[0]+"""?utm_source=generator' width="100%" height="380" frameBorder="0" allowtransparency="true" allow="encrypted-media"></iframe>""",height=300,scrolling=True)
    else:
        st.warning("Please add playlist link")

