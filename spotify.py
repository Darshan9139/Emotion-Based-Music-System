import streamlit as st
import streamlit.components.v1 as components

# bootstrap 4 collapse example
components.html("""
<iframe style="border-radius:12px" 
src="https://open.spotify.com/embed/playlist/2jbIbMfF6WxCEB5xArxXg6?utm_source=generator&theme=0" 
width="100%" height="700" frameBorder="0" allowfullscreen="" 
allow="autoplay; clipboard-write; encrypted-media; 
fullscreen; picture-in-picture"></iframe>""",height=100)
components.iframe('https://open.spotify.com/embed/playlist/2jbIbMfF6WxCEB5xArxXg6?utm_source=generator&theme=0',width=1000,height=1000)

components.html("""<iframe src="https://open.spotify.com/embed/playlist/2jbIbMfF6WxCEB5xArxXg6" width="100%" height="380" frameBorder="0" allowtransparency="true" allow="encrypted-media"></iframe>""",height=700)