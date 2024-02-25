files of interest:

- analyze/analysis.ipynb
- collect/script.py (note: unfortunately must be run from collect/)
- preprocess collected data with analyze/preprocess.py,  
  -o analyze/pre_bigdata
  (ten plik analizowany w analysis.ipynb)
- analyze/donwloads/download.py (not needed though, downloads some stuff that wasn't put to use)

note: need to add api_key in .env (create sibling to .env.example)

# setup

python3 -m venv /path/to/new/virtual/environment

<path_to_venv>/Scripts/activate

\# in the root directory!  
pip install -r requirements.txt

\# dla jupytera w vscode i w ogóle:  
ipython kernel install --user --name=autobusy

(potem wybierz to do wykonania)

after set up: in case of problems with python3, run everything using python, not python3 (sorry, not gonna fix it now)
