#!/bin/sh

eval "$(/$HOME/miniconda/bin/conda shell.bash hook)"

python3 rag-server.py&
streamlit run llm_ui.py
