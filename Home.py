import streamlit as st
import pandas as pd
import numpy as np
from streamlit_extras.card import card
from streamlit_extras.app_logo import add_logo
from streamlit_extras.switch_page_button import switch_page
import base64
import streamlit as st
from st_clickable_images import clickable_images
from database.db_utils import create_user
from streamlit_extras.add_vertical_space import add_vertical_space


create_user("Bob Baumeister", "bob.baumeister@some-comp.de")


st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)
add_logo("static/imgs/logo2.jpg", height=300)

st.write("# Welcome to JobSpeak! 👋")

st.sidebar.success("Choose your role.")


st.markdown(
    """
    ## Choose your role:
"""
)

# TODO make better pictures and edit text ontop of them with photoshop, etc...
images = []
for file in ["static/imgs/workers.jpg", "static/imgs/supervisor.jpg"]:
    with open(file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()
        images.append(f"data:image/jpeg;base64,{encoded}")

clicked = clickable_images(
    images,
    titles=["Workers", "Supervisor"],
    div_style={"display": "flex", "justify-content": "center", "flex-wrap": "wrap"},
    img_style={"margin": "10px", "height": "300px", "aspect-ratio": "1/1", "object-fit": "cover", "border-radius": "10px"},
)

if clicked == 0:
    switch_page("worker view")
elif clicked == 1:
    switch_page("supervisor view")

