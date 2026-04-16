# Commande pour executer ce script :
# docker exec -it app2_django sh -c "python manage.py shell < group_user_droits.py"

import os

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission


db_user = os.getenv("DB_USER")
if not db_user:
    raise RuntimeError("La variable d'environnement DB_USER est absente.")

# 1) Creer/recuperer le groupe visiteurs.
grp_visiteurs, _ = Group.objects.get_or_create(name="grp_visiteurs")

# 2) Attribuer tous les droits 'can view' (permissions 'view_*').
view_permissions = Permission.objects.filter(codename__startswith="view_")
grp_visiteurs.permissions.set(view_permissions)

# 3) Creer/mettre a jour l'utilisateur paul.
User = get_user_model()
paul, _ = User.objects.get_or_create(username="paul")
paul.set_password("mdppaul")
paul.is_active = True
paul.save()

# 4) Ajouter paul au groupe visiteurs.
paul.groups.add(grp_visiteurs)

print(f"DB_USER detecte : {db_user}")
print(f"Groupe '{grp_visiteurs.name}' configure avec {view_permissions.count()} droits view_.")
print("Utilisateur 'paul' cree/mis a jour et ajoute au groupe 'grp_visiteurs'.")
