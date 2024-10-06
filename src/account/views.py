from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import CustomUser
from .decorators import staff_required, redirect_authenticated_user
from django.contrib import messages
from django.views import View  # Ajoutez cette ligne

from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.conf import settings  # Ajout pour accéder aux paramètres

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.template import loader
from .forms import ChangeEmailForm
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.utils.dateparse import parse_date
from datetime import datetime
from .forms import CustomUserForm






@redirect_authenticated_user
def signup(request):
    if request.method == "POST":
        pseudo = request.POST.get("pseudo")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Les mots de passe ne sont pas identiques")
            return render(request, "account/signup.html")

        if CustomUser.objects.filter(pseudo=pseudo).exists():
            messages.error(request, "Le pseudo est déjà pris.")
            return render(request, "account/signup.html")

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "L'email est déjà utilisé.")
            return render(request, "account/signup.html")

        user = CustomUser(email=email, pseudo=pseudo)
        user.set_password(password1)
        user.is_active = False
        user.save()

        current_site = get_current_site(request)
        mail_subject = 'Activation de votre compte'
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = token_generator.make_token(user)
        verification_link = f"{request.scheme}://{current_site.domain}/account/verify-email/{uid}/{token}/"
        message = render_to_string('account/email_verification.html', {
            'user': user,
            'verification_link': verification_link,
        })

        email = EmailMultiAlternatives(
            mail_subject,
            message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[email]
        )
        email.attach_alternative(message, "text/html")

        try:
            email.send()
        except Exception as e:
            user.delete()
            messages.error(request, f"Erreur lors de l'envoi de l'email : {str(e)}")
            return render(request, "account/signup.html")

        messages.success(request, "Votre compte a été créé avec succès. Veuillez vérifier votre email pour confirmer votre inscription.")
        return redirect('login')

    return render(request, "account/signup.html")


@login_required
def update_user(request):
    user = request.user

    if request.method == "POST":
        form = CustomUserForm(request.POST, instance=user)

        if form.is_valid():
            form.save()
            messages.success(request, "Votre profil a été mis à jour avec succès.")
            return redirect('profile')
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = CustomUserForm(instance=user)

    return render(request, "account/update_user.html", {"form": form})

@redirect_authenticated_user
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')  # Rediriger vers le profil de l'utilisateur
        else:
            return render(request, "account/login.html", {"error": "Email ou mot de passe incorrect."})

    return render(request, "account/login.html")


def logout_view(request):
    logout(request)
    return redirect('login')  # Rediriger vers la page de connexion après la déconnexion


@login_required
def profile(request, user_id=None):
    if user_id:
        # Afficher le profil d'un utilisateur spécifique
        user_profile = get_object_or_404(CustomUser, id=user_id)
    else:
        # Afficher le profil de l'utilisateur connecté
        user_profile = request.user

    return render(request, 'account/profile.html', {'user': user_profile})


@staff_required
def list_user(request):
    users = CustomUser.objects.all()
    return render(request, 'account/user_list.html', {"users": users})


@login_required
def delete_user(request):
    if request.method == 'POST':
        user = request.user
        confirmation = request.POST.get('confirmation')
        username = request.POST.get('username')

        # Vérifiez la case de confirmation
        if confirmation != 'on':
            messages.error(request, 'Vous devez cocher la case pour confirmer la suppression.')
            return render(request, 'account/delete_user.html')

        # Vérifiez le pseudo
        if username != user.pseudo:
            messages.error(request, 'Le pseudo saisi ne correspond pas à votre pseudo exacte.')
            return render(request, 'account/delete_user.html')

        # Si toutes les conditions sont remplies, supprimez le compte
        user.delete()
        messages.success(request, 'Votre compte a été supprimé avec succès.')
        return redirect('index')  # Rediriger vers la page d'accueil après suppression

    return render(request, 'account/delete_user.html')


# Vue pour vérifier l'email
def verify_email(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, "Merci pour votre confirmation par email. Vous êtes maintenant connecté.")
        return redirect('profile')
    else:
        messages.error(request, "Le lien de confirmation est invalide ou a expiré.")
        return redirect('signup')



class CustomPasswordResetView(PasswordResetView):
    template_name = 'account/password_reset_form.html'
    email_template_name = 'account/password_reset_email.html'
    subject_template_name = "account/password_reset_subject.txt"
    success_url = reverse_lazy('password_reset_done')
    html_email_template_name = 'account/password_reset_email.html'

    def send_mail(self, subject_template_name, email_template_name, context, from_email, to_email, html_email_template_name=None):
        """
        Sends a django.core.mail.EmailMultiAlternatives to `to_email`.
        """
        subject = loader.render_to_string(subject_template_name, context)
        subject = ''.join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)
        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, 'text/html')
        email_message.send()

    def form_valid(self, form):
        opts = {
            'use_https': self.request.is_secure(),
            'token_generator': self.token_generator,
            'from_email': self.from_email,
            'email_template_name': self.email_template_name,
            'subject_template_name': self.subject_template_name,
            'request': self.request,
            'html_email_template_name': self.html_email_template_name,
        }
        form.save(**opts)
        return super().form_valid(form)

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'account/password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'account/password_reset_done.html'

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'account/password_reset_complete.html'

def test(request):
    return render(request, 'account/password_reset_email.html')




User = get_user_model()
class ChangeEmailView(View):
    @method_decorator(login_required)
    def get(self, request):
        form = ChangeEmailForm()
        return render(request, 'account/change_email.html', {'form': form})

    @method_decorator(login_required)
    def post(self, request):
        form = ChangeEmailForm(request.POST)
        if form.is_valid():
            new_email = form.cleaned_data['new_email']
            user = request.user
            user.temporary_email = new_email
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Confirmez votre nouvelle adresse email'
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = token_generator.make_token(user)
            confirmation_link = request.build_absolute_uri(
                reverse('confirm_email_change', kwargs={'uidb64': uid, 'token': token})
            )
            message = render_to_string('account/change_email_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': uid,
                'token': token,
                'protocol': 'https' if request.is_secure() else 'http',
                'confirmation_link': confirmation_link,
            })
            send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [new_email])
            messages.success(request, "Un email de confirmation a été envoyé à votre nouvelle adresse.")
            return redirect('email_change_done')
        return render(request, 'account/change_email.html', {'form': form})

class ConfirmEmailChangeView(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        if user is not None and token_generator.check_token(user, token):
            new_email = user.temporary_email
            old_email = user.email
            user.email = new_email
            user.temporary_email = ''
            user.save()
            mail_subject = 'Votre adresse email a été changée'
            message = render_to_string('account/email_change_notification.html', {
                'user': user,
                'new_email': new_email,
                'date': timezone.now(),
            })
            send_mail(mail_subject, message, settings.DEFAULT_FROM_EMAIL, [old_email])
            messages.success(request, "Votre adresse email a été mise à jour avec succès.")
            return redirect('email_change_complete')
        else:
            messages.error(request, "Le lien de confirmation est invalide ou a expiré.")
            return render(request, 'account/email_change_invalid.html')