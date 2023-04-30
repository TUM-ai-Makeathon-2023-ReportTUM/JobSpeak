# JobSpeak

Our submission to the 2023 April TUM-ai Makeathon


## Installation

```bash
conda create -n JobSpeak Python=3.10
conda activate JobSpeak
pip install streamlit --upgrade
pip install streamlit-extras
pip install st-clickable-images
pip install audio-recorder-streamlit

pip install SQLAlchemy
pip install pdfkit
pip install pypdf

pip install cohere
pip install numpy


pip install azure-cognitiveservices-vision-computervision
```


## Running

From the root folder run:

```bash
streamlit run Home.py
```

Using the APIs requires adding all keys in `env.py`.
