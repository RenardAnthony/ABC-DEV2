"""
URL configuration for TestUtilisateur project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from TestUtilisateur import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    path('account/', include('account.urls')),  # Include les urls de l'application account
    path('profiles/', include('user_profiles.urls')), # Include les urls de l'application profile utilisateur
    path('gun/', include('gun.urls')), # Include les urls de l'application gun (répliques)
    path('evenement/', include('evenement.urls')), # Include les urls de l'application evenement
    path('todo/', include('todo.urls')), # Application todoliste
    path('gestion_projet/', include('gestion_projet.urls')), # Application gestion projet
    path('regles/', include('regles.urls')),

    path('test/', views.test, name="test"), #Page vierge juste pour les test

    path('', views.index, name='index'),  # URL pour la page d'accueil

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
