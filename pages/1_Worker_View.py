import streamlit as st
import time
import numpy as np
from dataclasses import dataclass
import streamlit as st
import wave

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

SPEECH_WAV_FILENAME = "worker_report_voice_recording.wav"

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
if 'submission_success' not in st.session_state:
    st.session_state.submission_success = False
if 'transcribed_text' not in st.session_state:
    st.session_state.transcribed_text = ""

# Helper functions
def set_view_start():
    st.session_state.displayed_elements = _VIEW_START
    # Clear inputs and reset
    st.session_state.entered_task_keys_and_text = {}
    st.session_state.transcribed_text = ""
    st.session_state.submission_success = False
    
def set_view_written_input():
    st.session_state.displayed_elements = _VIEW_WRITTEN_INPUT

def set_view_speech_input():
    st.session_state.displayed_elements = _VIEW_SPEECH_INPUT
    
def set_view_report_submission():
    st.session_state.displayed_elements = _VIEW_REPORT_SUBMISSION
    
def is_submission_successful():
    return st.session_state.submission_success

def set_submission_successful(flag):
    assert isinstance(flag, bool)
    st.session_state.submission_success = flag

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
    
def get_transcribed_text():
    return st.session_state.transcribed_text
    
# Helper functions for rendering pages

def show_start_elements():
    """The start page"""
    
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
    """The edit page for written text"""
    
    st.markdown(f"## Writing Report: {st.session_state.given_report_name}")
    st.markdown("### What did you work on today?")
    
    add_vertical_space(LARGE_SEP_N_LINES)
    
    # Create List of task boxes
    d = get_entered_task_keys_and_text()
    next_disabled = True
    for idx, (task_key, task_text) in enumerate(d.items()):
        if task_text != '':
            next_disabled = False
        col1, col2 = st.columns([1, 6])
        with col1:
            st.write(f"No. {idx+1}")
        with col2:
            st.text_input("Enter some text", task_text, key=task_key, label_visibility="collapsed")
            add_task_key_and_text(task_key, task_text)
    
    add_vertical_space(LARGE_SEP_N_LINES)

    col1, col2 = st.columns(2)
    with col1:
        st.button("🔙 Back", on_click=set_view_start)
    with col2:
        st.button("Next ✅", on_click=set_view_report_submission, disabled=next_disabled)

    
def show_speech_input_elements():
    """The edit page for speech"""
    
    st.markdown(f"## Report: {st.session_state.given_report_name}")
    st.markdown("### What did you work on today?")
    add_vertical_space(LARGE_SEP_N_LINES)

    def record():
        audio_bytes = audio_recorder()
        if audio_bytes:
            st.audio(audio_bytes)
        return audio_bytes

    # Create Microphone
    # audio_data = record()
    next_disabled = True
    
    audio_data = st_audiorec()
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
    
    if audio_data is not None:
        st.audio(audio_data, format='audio/wav')
        # Save as .wav file
        if os.path.exists(SPEECH_WAV_FILENAME):
            os.remove(SPEECH_WAV_FILENAME)
        with open(SPEECH_WAV_FILENAME, mode='bx') as f:
            f.write(audio_data)

        with wave.open(SPEECH_WAV_FILENAME, 'r') as wav_file:
            frames = wav_file.getnframes()
            rate = wav_file.getframerate()
            duration = frames / float(rate)
            if duration > 1: # in seconds
                next_disabled = False
    
    add_vertical_space(LARGE_SEP_N_LINES)

    
    col1, col2 = st.columns(2)
    with col1:
        st.button("🔙 Back", on_click=set_view_start)
    with col2:
        st.button("Next ✅", on_click=set_view_report_submission, disabled=next_disabled)
    
def show_report_submission_elements():
    """The Submission page"""
    
    st.markdown(f"## Submit Report: {st.session_state.given_report_name}")
    
    add_vertical_space(LARGE_SEP_N_LINES)
    
    # Display a list of bullet points        
    markdown_str = ""
    is_transcribed = False
    if get_transcribed_text():
        is_transcribed = True
        markdown_str = get_transcribed_text()
    else:
        for k, v in get_entered_task_keys_and_text().items():
            if v != '':
                markdown_str += f"- {v}\n"
            
    st.markdown(markdown_str)
    
    add_vertical_space(LARGE_SEP_N_LINES)
    
    # Display Cancel, Edit and Submit buttons
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.button("❌ Cancel", on_click=set_view_start, disabled=is_submission_successful())
    with col2:
        on_click_func = show_speech_input_elements if is_transcribed else set_view_written_input
        st.button("Edit", on_click=set_view_written_input, disabled=is_submission_successful())
    with col3:
        def on_click_submit():
            # with st.spinner('Wait for it...'):
            #     time.sleep(5)
            rain(
                emoji="🎉",
                font_size=54,
                falling_speed=5,
                animation_length=5,#"infinite",
            )
            set_submission_successful(True)
            
        st.button("Submit ✅", on_click=on_click_submit, disabled=is_submission_successful())
    
    if is_submission_successful():
        st.button("Go Back 🏠", on_click=set_view_start)


### RENDERING ALL CODE

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

    