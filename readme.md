26/01/2026 : Créé par Julien Besombes













# Installer l'application sur Windows : 

## Creer un dossier / Utiliser un dossier avec les différents projets
par exemple : mes_applis_web

## Ouvrir le dossier avec Visual Studio Code (ou autres)

## Ouvrir un terminal dans Visual Studio Code (ou autres) :

et lancer les commandes suivantes : 

    ### Windows :

    git clone https://github.com/dojo360-git/gestom_django.git
    cd gestom_django
    python3 -m venv .venv
    .\.venv\Scripts\Activate.ps1
    pip install -r requirements.txt


    ### Linux Debian/Ubuntu :

    git clone https://github.com/dojo360-git/gestom_django.git
    cd gestom_django
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt


## Création du fichier .env et des infos base de données Postgre

26/01/2026 : la base tourne pour le moment avec sqlite3 proposée par le Fraework Django 

En vue de la connection à une base postgre : 

    @"
    DEBUG=True
    SECRET_KEY=django-insecure-xxxx
    DATABASE_URL=postgres://user:password@localhost:5432/dbname
    "@ | Out-File -Encoding utf8 .env

    .env à ouvrir et à modifier 



# Lancer l'application :

Nécéssite que gestom_django ait été installé 

ouvrir le dossier gestom_django avec Visual Studio Code 
Lancer un terminal : Terminal / New terminal : 

    python manage.py runserver

Ouvrir un navigateur sur : 

    http://127.0.0.1:8000/


Let's go ! 





# Autres
python manage.py shell

