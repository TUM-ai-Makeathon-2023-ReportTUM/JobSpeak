import streamlit as st
import time
import numpy as np
from dataclasses import dataclass
import streamlit as st

# from 
# https://github.com/Joooohan/audio-recorder-streamlit
from audio_recorder_streamlit import audio_recorder

# Import for Audio Recorder from
# https://github.com/stefanrmmr/streamlit_audio_recorder
import os
import numpy as np
import streamlit as st
from io import BytesIO
import streamlit.components.v1 as components
from st_audiorec.st_custom_components import st_audiorec

from streamlit_extras.add_vertical_space import add_vertical_space
from streamlit_card import card
from streamlit_extras.let_it_rain import rain





_VIEW_START = "start"
_VIEW_WRITTEN_INPUT = "report_input"
_VIEW_SPEECH_INPUT = "report_speech_input"
_VIEW_REPORT_SUBMISSION = "report_submission"

# STYLING
LARGE_SEP_N_LINES = 5

# Initialize the Session State
# session_state = st.session_state
if 'displayed_elements' not in st.session_state:
    st.session_state.displayed_elements = _VIEW_START
if 'entered_task_keys_and_text' not in st.session_state:
    st.session_state.entered_task_keys_and_text = {}
if 'given_report_name' not in st.session_state:
    st.session_state.given_report_name = None

# Helper functions
def set_view_start():
    st.session_state.displayed_elements = _VIEW_START
def set_view_written_input():
    st.session_state.displayed_elements = _VIEW_WRITTEN_INPUT

def set_view_speech_input():
    st.session_state.displayed_elements = _VIEW_SPEECH_INPUT
    
def set_view_report_submission():
    st.session_state.displayed_elements = _VIEW_REPORT_SUBMISSION

def get_entered_task_keys_and_text():
    """
    Removes empty entries. 
    And this save the current values from the keys into the dict stored for this user's session!
    """
    d = st.session_state.entered_task_keys_and_text
    ret = {}
    make_key = lambda i: f"task_text_field_key_{i}"
    idx = 0
    for k, v in d.items():
        idx += 1
        # If there is a value entered in this box that is not in the session dict yet, then keep it
        if st.session_state.get(k, "") != '':
            ret[make_key(idx)] = st.session_state[k]
        elif v != '':
            ret[k] = v
    # Copy all current values into session dict
    st.session_state.entered_task_keys_and_text = ret
    # Add final empty box
    ret[make_key(idx+1)] = ""
    return ret

def add_task_key_and_text(key, text):
    st.session_state.entered_task_keys_and_text[key] = text

def show_start_elements():
    st.markdown("## Begin a new Report")
    st.write(
        """some text about this blablabla"""
    )
    st.text_input("Report name", placeholder="Give the report a name...", key="report_name_text_field")
    
    enabled = (
        isinstance(st.session_state.report_name_text_field, str) and 
        st.session_state.report_name_text_field
    )
    st.session_state.given_report_name = st.session_state.report_name_text_field
    
    st.text("Add tasks:")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("📲 By Writing", on_click=set_view_written_input, disabled=not enabled)
    with col2:
        st.button("🗣️ By Speaking", on_click=set_view_speech_input, disabled=not enabled)
    with col3:
        st.button("📝 By Photo", on_click=lambda: None, disabled=not enabled)


def show_written_input_elements():
    
    st.markdown(f"## Writing Report: {st.session_state.given_report_name}")
    st.markdown("### Add Your Tasks")
    
    add_vertical_space(LARGE_SEP_N_LINES)
    
    # Create List of task boxes
    d = get_entered_task_keys_and_text()
    for idx, (task_key, task_text) in enumerate(d.items()):
        col1, col2 = st.columns([1, 6])
        with col1:
            st.write(f"No. {idx+1}")
        with col2:
            st.text_input("Enter some text", task_text, key=task_key, label_visibility="collapsed")
            add_task_key_and_text(task_key, task_text)
    
    add_vertical_space(LARGE_SEP_N_LINES)

    col1, col2 = st.columns(2)
    with col1:
        st.button("🔙 Back to Start", on_click=set_view_start)
    with col2:
        st.button("✅ Review", on_click=set_view_report_submission)

    
def show_speech_input_elements():
    st.markdown(f"## Report: {st.session_state.given_report_name}")
    st.markdown("### What did you work on today?")
    add_vertical_space(LARGE_SEP_N_LINES)

    
    def record():
        audio_bytes = audio_recorder()
        if audio_bytes:
            st.audio(audio_bytes)
        return audio_bytes

    audio_data = record()
    
    add_vertical_space(LARGE_SEP_N_LINES)
    
    
    # wav_audio_data = st_audiorec()
    # if wav_audio_data is not None:
    #     # display audio data as received on the backend
    #     st.audio(wav_audio_data, format='audio/wav')
        
    #     # wavfile.write('abc1.wav', 41_000, wav_audio_data)
    #     if os.path.exists('myfile.wav'):
    #         os.remove("myfile.wav")
    #     with open('myfile.wav', mode='bx') as f:
    #         f.write(wav_audio_data)
        
    # INFO: by calling the function an instance of the audio recorder is created
    # INFO: once a recording is completed, audio data will be saved to wav_audio_data
    
    col1, col2 = st.columns(2)
    with col1:
        st.button("🔙 Back to Start", on_click=set_view_start)
    with col2:
        st.button("✅ Review", on_click=set_view_report_submission)
    
def show_report_submission_elements():
    st.markdown(f"## Review Report: {st.session_state.given_report_name}")
    col1, col2, col3 = st.columns(3)
    
    rain(
        emoji="🎈",
        font_size=54,
        falling_speed=5,
        animation_length="infinite",
    )   
    with col1:
        st.button("Cancel", on_click=set_view_start)
    with col2:
        st.button("Edit", on_click=set_view_written_input)
    with col3:
        st.button("Submit", on_click=set_view_report_submission)


### RENDERING CODE

# Page Setup
st.set_page_config(page_title="Worker View", page_icon="👷")
st.sidebar.header("Worker View")
st.markdown("# Worker View")

if st.session_state.displayed_elements == _VIEW_START:
    show_start_elements()
elif st.session_state.displayed_elements == _VIEW_WRITTEN_INPUT:
    show_written_input_elements()
elif st.session_state.displayed_elements == _VIEW_SPEECH_INPUT:
    show_speech_input_elements()
elif st.session_state.displayed_elements == _VIEW_REPORT_SUBMISSION:
    show_report_submission_elements()

    