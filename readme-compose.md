# __dev__ sur PC windows  :

## Prérequis : 

### Installer DockerDesktop sur windows (Si besoin) :

```bash 
winget install -e --id Docker.DockerDesktop 
```

### Mettre à jour émulateur WSL (Si besoin) :

```bash
wsl.exe --update
```
## Installation : 

### Installer VS code, lancer VS Code et ouvrir un terminal PS :

### Cloner le projet :

``` 
git clone https://github.com/dojo360-git/gestom_django.git  app2_regie
cd app2_regie
```
### Lancer docker compose __dev__

``` 
docker compose -f docker-compose__dev__.yml up -d --build
docker compose -f docker-compose__dev__.yml up -d
``` 

## Lancer l'appli dans un navigateur : 

http://127.0.0.1:8000/

## Ajouter des users : 

http://127.0.0.1:8000/admin

user : 
```
superadmin
```
mdp : 
```
SuperMotDePassePour2026!*
```


## Autres : 
### Lister mes containers : 
```
docker ps -a --filter "name=^app2"
```

### Lister les reseaux : 
```
docker network ls
```
