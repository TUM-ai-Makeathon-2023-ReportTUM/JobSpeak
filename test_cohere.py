"""
Functionality to get summaries in the form of bulletpoints and formal reports from
either transcribed audio recordings from workers or by handwritten-notes taken
from the workers in the form of bullet points.

Input (defined as arbitrary values in the current script):
input_text: str, the text that the NLP pipeline is supposed to process.
usecase: str, either A or B. A is for the case that we input transcriptions of audio data
        B is for the case that we provide the bulletpoints that were extracted from the
        handwriting of the worker.
date: str, the date to append to the automatically inferred title 
lambda_consistency: float, weighting term of the consistency error
lambda_faith:       float, weighting term of the faithfulness error 

Output:
bullet_list:    [str], list of strings with each bullet point as an element
summary_report: str, summary of the input text in formal language and in paragraph form
title: str, inferred report title based on input text with the current date prepended

total_error: custom error term to measure how consistent the model is and how faithful the outputs are to the
            original input.
"""
import numpy as np
import cohere
import nlp.use_llm as llm
# Replace this with the output from whisper or OCR model
input_text = "My first travel to the site, which required a 1.5 hour drive, there was some traffic. I conducted a safety inspection before beginning to work by looking at the three turbines from the ground. No issues found. Then started inspection on turbine number 456. While inspecting the turbine I found damages on the blades. They were a little rusty. Oh no. I mean, they were mainly damaged. I performed a superficial repair using resin on the blade. Afterwards I checked the gearbox and lubrication on number 789. There was some leak. It got my clothes all dirty"

# Replace this with the list of strings we get from the app
input_list = ["task_1", "task_2", "task_3"]

# Input date
date = "29.04.2023"

results_a = llm.process_case_A(input_text, date)
results_b = llm.process_case_B(input_list, date)
