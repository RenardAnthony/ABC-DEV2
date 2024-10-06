from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.utils import timezone

class MyUserManager(BaseUserManager):

    def create_user(self, email, password=None, pseudo=None):
        if not email:
            raise ValueError("Vous devez entrer un email unique.")
        if not pseudo:
            raise ValueError('Users must have a pseudo')

        user = self.model(
            email=self.normalize_email(email),
            pseudo=pseudo
        )

        user.set_password(password)
        user.is_active = False  # Par défaut, le compte n'est pas actif tant que l'email n'est pas vérifié
        user.save(using=self._db)
        return user


    def create_superuser(self, email, password=None, pseudo=None):
        user = self.create_user(email=email, password=password, pseudo=pseudo)
        user.is_admin = True
        user.is_staff = True
        user.is_active = True  # Les superutilisateurs sont actifs dès leur création
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):

    email = models.EmailField(
        unique=True,
        max_length=255,
        blank=False
    )

    pseudo = models.CharField(
        unique=True,
        max_length=25,
        blank=False
    )

    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )

    temporary_email = models.EmailField(blank=True, null=True)

    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["pseudo"]

    objects = MyUserManager()

    class Meta:
        verbose_name = "Utilisateur"

    def __str__(self):
        return self.pseudo

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True