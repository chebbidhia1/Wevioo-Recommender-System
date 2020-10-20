#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
from Wevioo import RecommendationModel1,RecommendationModel3
import pickle
import pandas as pd
with open ('Data/ProfilsIdeaux', 'rb') as fp:
    profilIdeaux = pickle.load(fp)

with open ('Data/profil_type', 'rb') as fp:
    profil_type = pickle.load(fp)

df = pd.read_csv("Data/df_final_2.csv")
candidat = pd.read_csv("Data/candidats.csv")


"""
rec = RecommendationModel1(profilIdeaux,df)
with open ('Data/RecommendationModel1', 'wb') as fp:
    pickle.dump(rec,fp)
"""

#rec2 = RecommendationModel3(profil_type,candidat,df)

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'MyFirstTest.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
