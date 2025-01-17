### On a un nouveau systeme de "permission" qui permet de ne pas passer n'import qui staff



#
#### 5 Permissions:
- hab_orga *(peut cree, supprimer, modifier des événement)*
- hab_chrony *(peut valider les chrony pour des événement)*
- hab_payment *(peut valider les payment pour des événement)*
####
- hab_secu *(peut faire le briff securiter,)*
- hab_loc *(peut faire le briff location)*

(*hab_secu* et *hab_loc* ont pour le moment aucun intérêt sur le site, mais ça peut permetre sur chaque evenement de s'assurer d'avoir une personne habiliter)


#
#
# Pour les utiliser on a un systeme backend et un frond-end

#
## *Backend*
**Dans la views on block le chargement de cette dernière si la permission n'est pas accorder**
    
    ################

    #Verifier permission de l'utilisateur

    user_profile = request.user.userprofile
    if user_profile.role != "staff" and not (
            user_profile.has_permission("hab_orga") or
            user_profile.has_permission("hab_chrony") or
            user_profile.has_permission("hab_payment")
    ):
        return HttpResponseForbidden("Vous n'avez pas la permission d'accéder à cette page.")
    
    ################

#
## *Front-end*
**Dans la views on crée une variable bool true si l'utilisateur a la bonne permission. On la passe ensuite en argument pour afficher ou non un element.**
    
    # Vérification des permissions côté back-end

    ma_variable = False
    if request.user:
        if request.user.is_staff:
            ma_variable = True
        else:
            try:
                user_profile = request.user.userprofile
                if user_profile.has_permission("hab_orga") or user_profile.has_permission("hab_payment"):
                    ma_variable = True
            except UserProfile.DoesNotExist:
                pass

    return render(request,  [...], {
        'ma_variable': ma_variable,
    })

puis, côté front-end

    {% if ma_variable %}
        <p>Mon element ici</p>
    {% endif %}


### Le "is_staff" passe au dessus de tout les permission alors attention !

#
#