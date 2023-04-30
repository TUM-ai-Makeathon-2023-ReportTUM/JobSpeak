import streamlit as st
import time
import numpy as np
from dataclasses import dataclass
import streamlit as st
import wave
import datetime

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

from ml_models.whisper_voice2text import query_hf
from ml_models.use_llm import process_case_A, process_case_B
from sys import platform
if platform != "darwin":  # not OS X
    from ml_models.ocr import query_ocr
from ml_models.translate import query_translate

from database.db_utils import create_report
from PIL import Image


_VIEW_START = "start"
_VIEW_WRITTEN_INPUT = "report_input"
_VIEW_SPEECH_INPUT = "report_speech_input"
_VIEW_CAMERA_INPUT = "report_camera_input"
_VIEW_REPORT_SUBMISSION = "report_submission"

SPEECH_WAV_FILENAME = "worker_report_voice_recording.wav"
IMG_JPG_FILENAME = "worker_report_image.jpg"

# STYLING
LARGE_SEP_N_LINES = 5
SMALL_SEP_N_LINES = 2

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

def set_view_camera_input():
    st.session_state.displayed_elements = _VIEW_CAMERA_INPUT
    
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

def set_transcribed_text(text):
    st.session_state.transcribed_text = text
    
def get_given_report_name():
    return st.session_state.given_report_name
    
    
# Helper functions for rendering pages

def show_start_elements():
    """The start page"""
    
    st.markdown("## Begin a new Report")
    # st.write(
    #     """"""
    # )
    st.sidebar.success("Begin your report.")
    
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
        st.button("📸 By Photo", on_click=set_view_camera_input, disabled=not enabled)


def show_written_input_elements():
    """The edit page for written text"""
    
    st.markdown(f"## Writing Report: {st.session_state.given_report_name}")
    st.markdown("### What did you work on today?")
    st.sidebar.success("Enter your achievements.")
    
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
    st.sidebar.success("Enter your achievements.")
    
    add_vertical_space(SMALL_SEP_N_LINES)
    
    st.markdown("**Hints**:")
    st.markdown("- If recording does not start the first time, press 'Stop' and then press 'Start' again.")
    st.markdown("- Unfortunately our Voice2text model only works with audio <30sec. and longer messages work better.")
    st.markdown("- If you get the error 'Model ... is currently loading', wait 20sec and try again.")
    
    add_vertical_space(SMALL_SEP_N_LINES)

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
                # Pass file to speech2text model
                with st.spinner('Running Voice2Text. Please wait...'):
                    response = query_hf(SPEECH_WAV_FILENAME)
                    try:
                        set_transcribed_text(response["text"])
                        next_disabled = False
                    except KeyError:
                        st.sidebar.error(f"Voice2Text failed: {response}.")
                    
    add_vertical_space(LARGE_SEP_N_LINES)

    col1, col2 = st.columns(2)
    with col1:
        st.button("🔙 Back", on_click=set_view_start)
    with col2:
        st.button("Next ✅", on_click=set_view_report_submission, disabled=next_disabled)
        

def show_view_camera_input():
    """Input page from captured image."""
    
    st.markdown(f"## Report: {st.session_state.given_report_name}")
    st.markdown("### What did you work on today?")
    st.sidebar.success("Upload an image of handwritten notes.")
    
    add_vertical_space(LARGE_SEP_N_LINES)
    
    next_disabled = True
    uploaded_file = st.file_uploader("Supported types: png, jpg, jpeg", type=["png", "jpg", "jpeg"])
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        if os.path.exists(IMG_JPG_FILENAME):
            os.remove(IMG_JPG_FILENAME)
        image.save(IMG_JPG_FILENAME)

        col1, col2 = st.columns(2)
        with col1:
            st.markdown('<p style="text-align: center;">Before</p>',unsafe_allow_html=True)
            st.image(image,width=300) 
        with col2:
            result_text = ""
            with st.spinner('Running Img2Text. Please wait...'):
                try:
                    result_text, bboxes = query_ocr(IMG_JPG_FILENAME)
                    set_transcribed_text(result_text)
                    next_disabled = False
                except Exception as e:
                    st.sidebar.error(f"Img2Text failed: {e}.")
            st.text_area(result_text) 
        
    add_vertical_space(LARGE_SEP_N_LINES)

    col1, col2 = st.columns(2)
    with col1:
        st.button("🔙 Back", on_click=set_view_start)
    with col2:
        st.button("Next ✅", on_click=set_view_report_submission, disabled=next_disabled)
    
      
def show_report_submission_elements():
    """The Submission page"""
    
    st.markdown(f"## Submit Report: {st.session_state.given_report_name}")
    st.sidebar.success("Submit your report.")
    
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
        if is_transcribed:
            on_click_func = show_speech_input_elements
            button_name = "Try Again"
        else:
            on_click_func = set_view_written_input
            button_name = "Edit"
        st.button(button_name, on_click=on_click_func, disabled=is_submission_successful())
    with col3:
        def on_click_submit():
            with st.spinner('Running Text2Text. Please wait...'):
                success = False
                # If we have free text
                if get_transcribed_text():
                    try:
                        results_dict = process_case_A(get_transcribed_text())
                        summary_report = results_dict["summary_report"]
                        success = True
                    except Exception as e:
                        st.sidebar.error(f"Process A Failed: {e}.")
                else:
                    # If we have a list
                    task_list = [v for k, v in get_entered_task_keys_and_text().items() if v != '']
                    try:
                        results_dict = process_case_B(task_list)
                        summary_report = query_translate(results_dict["summary_report"], source_language="es", dest_language="en")
                        success = True
                    except Exception as e:
                        st.sidebar.error(f"Process B Failed: {e}.")

                # Write results_dict to DB
                if success:
                    create_report(
                        report_name=get_given_report_name(),
                        user_id="1",        # always same
                        summary=summary_report,
                        date=datetime.datetime.now().strftime("%Y-%m-%d"),       # e.g. 2021-01-01
                        img_path="",
                        score=results_dict["error"],
                    )
                
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
elif st.session_state.displayed_elements == _VIEW_CAMERA_INPUT:
    show_view_camera_input()
elif st.session_state.displayed_elements == _VIEW_REPORT_SUBMISSION:
    show_report_submission_elements()

    