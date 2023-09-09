from django.db import models
from django.contrib.auth.models import User


class UserProfile(User):
    has_changed_password = models.BooleanField(default=False)