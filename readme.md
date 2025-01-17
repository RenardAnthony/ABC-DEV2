*Très bien je n'est pas l'habitude de faire un readme.md propre et la je le fait tard dans le processus on va faire comme on peut...*

#


___
## 1.Installation

Une fois les fichiers installer et le serveur lancer il y a deux "commandes" à effectuer.<br>
Assuez vous d'avoir **is_staff** *et* **is_admin** actif sur votre compte.
###


>### Pour initialiser tous les terrains d'Airsoft rendez-vous sur la page <br>
>
>   >www.domain.com/evenement/remplir-bdd-lieux/
>
>Automatiquement le terrain de Cézac et les terrains de Reignac seront créé grace au fichier suivant :
>
> src/evenement/views.py /: def remplir_bdd_lieux

>### Pour initialiser toutes les permission des utilisateurs rendez-vous sur la page <br>
> www.domain.com/profiles/populate_roles/
>
>Automatiquement les permissions de base seront créé grace au fichier
>  
>> src/user_profiles/views.py /: def populate_role_permissions
>
>**Il est recommander de ne surtout pas modifier cette views !**
> Les permission sont codé en dur dans les views.

___

## 2.Structure utilisateur

Il y a deux tables dans la base de donnée pour gérer les utilisateurs.

- **"account_customuser"** La première est principal - gérer par l'application **>account<** <br> Elle stoque les informations de connection de l'utilisateur (email, pseudo, mdp, et les droit administrateur)
- **"user_profiles_userprofile"** gérer par l'application **>user_profiles<** <br> Elle stoque elle les informations "utilitaire" de notre utilisateur. (role, permission, photo de profil, biographie etc.)

___

## 3. Les autres données

Il y a bien d'autres tables dans notre base de donnée. en voici expliquer quellque une.

- **"gun_gun"** est utiliser pour stoquer les information concernant les répliques de nos utilisateur (puissance, type, photo) elle est lieu via un id a un utilisateur
- **"evenement_"** des tables evenement il y en a beaucoup. la principales est **evenement_evenement** qui stoque tout les venement et partie.
- **"gestion_projet"** est une application externe que j'ai developper pour suivre le developpement... du projet... Elle a rien a voir directement avec notre site d'airsoft mais peut être utiliser comme interface de gestion entre developpeurs.
- **"badges_badge"** stoque tout les badge qui existe et on peut en crée autemps que on veut.
- **"badges_userbadge"** stoque quelle utilisateur posed quelle badge. elle est lieu via un id à un utilisateur

Bien évoidament, en cas de suppression d'un compte utilisateur, en cascade, on suprime ces répliques, ces inscription au parties, ces badges, et tout ces fichiers stoquer sur le site (photo de réplique, photo de profil)
Dans le cas ou cette supression de media n'est pas automatique : > voir partie 4.

___

## 4. Page /admin

Cette page n'est accessible que au is_admin is_staff via l'url 
> www.domain.com/admin

>### Netoyage
> Si vous voulez faire une peut de netoyage dans les fichier du site.
> (et je recommande de le faire une a deux fois par an) il existe 2 commandes qui vous aideron.
> ### 1 Netoyage des images de répliques
> - Rendez-vous sur la page admin
> - Rendez-vous dans la partie "Gun -> Réplique"
> - Selectionnez toutes les répliques
>> - **! ATTENTION À NE PAS MISCLICK !**
>> - Dans le menu superieur "Action :" sélectionner : "Supprimer les images non utilisées"
>
> Cette action suprimera les images des répliques qui on été suprimer, ou les images remplacer.
> #
> ### 2 Netoyage des avatar utilisateur
> - Rendez-vous sur la page admin
> - Rendez-vous dans la partie "USER_PROFILES -> User Profiles"
> - Selectionnez tout les utilisateurs
>> - **! ATTENTION À NE PAS MISCLICK !**
>> - Dans le menu superieur "Action :" sélectionner : "Supprimer les images non utilisées"
>###
> Cette action suprimera les images des utilisateur qui on été suprimer, ou les images remplacer.


>### Permission
> Pour donner les permission a un utilisateur 2 solutions.
>> - Dans le cas ou cette utilisateur fait partie de l'administration de l'asso ou du developpement du site web. passer le is_admin is_staff depuis "ACCOUNT -> Utilisateurs"
>> - Dans tout les cas contraire utiliser le systeme de permission aproprier ->
> - Rendez-vous sur la page admin
> - Rendez-vous dans la partie "USER_PROFILES -> User Profiles"
> - Selectionner votre utilisateur
> - Dans la liste deroulante "Role permissions :" selectionner les permissions à accorder. (Ctrl+click)
> - Oubliez pas de valider en bas de la page.
> Félisitation, cette utilisateur à desormer des droit
 

>### Badges
>> ### 1. Crée un badge
>> C'est on ne peut plus simple
>> - Rendez-vous sur la page admin
>> - Rendez-vous dans la partie "BADGES -> Badges"
>> - En haut a droit "AJOUTER BADGE +"
>> - Donnez-lui un Name (ex : Un an de fidélité !)
>> - Donnez-lui une Description (ex : Être membre actif depuis un an.)
>> - Donnez-lui une Rarity (1 c'est pas rare, 5 c'est très rare)
>> - Donnez-lui une Image (un .jpg transparent de preferance)
>
>> ### 2. Donner un badge à un utilisateur manuellement
>> C'est encore plus simple
>> - Rendez-vous sur la page admin
>> - Rendez-vous dans la partie "BADGES -> USer badges"
>> - En haut a droit "AJOUTER USER BADGE +"
>> - Selectionner l'utilisateur et le badge à lui donner
>> - "is selected" indique si le badge sera afficher sur son profil ou simplement dans son inventaire. Attention, un utilisateur ne peut afficher que 3 badge a la fois, si vous ne forcé 4 je ne sais pas ce qu'il va ce passer :x


#
#
#