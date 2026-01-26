# Ouvrir un terminal dans Visual Studio Code (ou autres) :

git clone https://github.com/dojo360-git/gestom_django.git

cd gestom_django

python3 -m venv .venv

.\.venv\Scripts\Activate.ps1

pip install -r requirements.txt


## Création du fichier .env et des infos base de données : A mettre à jour 

@"
DEBUG=True
SECRET_KEY=django-insecure-xxxx
DATABASE_URL=postgres://user:password@localhost:5432/dbname
"@ | Out-File -Encoding utf8 .env

.env à ouvrir et modifier


# Lancer le serveur web :
python manage.py runserver

# Ouvrir un navigateur sur http://127.0.0.1:8000/





# Autres
python manage.py shell

