import pickle
from pathlib import Path
import streamlit_authenticator as stauth

teams = ['CAD','SOFTWARE','HARDWARE','ADMIN','VISION','GESTIONE']
usernames = ['CAD_team','SFTW_team','HRDW_team','Admin','VISION_team','GST_team']
passwords = ['Cad2023','Sftw2023','Hrdw2023','admin2023','Vision2023','Gestione2023']

hashed_password = stauth.Hasher(passwords).generate()

file_path = Path(__file__).parent / "hashed_pw.pkl"
with file_path.open("wb") as file:
    pickle.dump(hashed_password,file)