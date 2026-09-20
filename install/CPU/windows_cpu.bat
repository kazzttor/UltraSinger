@echo off
cd ..
cd ..
py -3.12 -m venv .venv
call .venv\Scripts\activate
python -m pip install -r requirements.txt
python -m pip install torch==2.8.0 torchaudio==2.8.0 --index-url https://download.pytorch.org/whl/cpu