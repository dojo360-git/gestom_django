26/01/2026 : Créé par Julien Besombes





# Pré requis : 

Ce projet nécessite Git et Python ≥ 3.12 

Ton projet utilise Django 6.0.1 → Python ≥ 3.12 obligatoire.



# Installer l'application gestom_django depuis repo Github : 

## Creer un dossier / Utiliser un dossier avec les différents projets appli web :
par exemple : mes_applis_web

## Ouvrir le dossier avec Visual Studio Code (ou equivalent)

## Ouvrir un terminal dans Visual Studio Code (ou equivalent) :

et lancer les commandes suivantes : 

    ### 🪟 Windows :

    git clone https://github.com/dojo360-git/gestom_django.git
    cd gestom_django
    python3 -m venv .venv
    .\.venv\Scripts\Activate.ps1
    pip install -r requirements.txt


    ### 🐧 Linux Debian/Ubuntu :

    git clone https://github.com/dojo360-git/gestom_django.git
    cd gestom_django
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt


## Création du fichier .env et des infos base de données Postgre

26/01/2026 : la base tourne pour le moment avec sqlite3 proposée par le Fraework Django 


Creer le .env a la racine du projet :

gestom_django/
├── .env                👈 ICI (IMPORTANT)
├── manage.py


et y coller les infos suivantes : avec les mots de passe renseignés
DEBUG=True
SECRET_KEY=django-insecure-XXXX



DATABASE_URL=postgres://u_pgd:PASSWORD@10.153.32.49:5432/ztest
DB_NAME=ztest
DB_USER=u_pgd
DB_PASSWORD=XXXX
DB_HOST=10.153.32.49
DB_PORT=5432



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







# Maintenance : 



python manage.py test core