# from django.contrib.auth.models import AbstractUser
# from django.core.validators import RegexValidator
# from django.db import models

# # class User(AbstractUser):
# #     phone = models.CharField(max_length=20, blank=True)

#     def __str__(self):
#         return self.username

# phone_validator = RegexValidator(
#     regex=r'^\+375(25|29|33|44)\d{7}$',
#     message="Введите номер в формате +375447410212"
# )

# class User(AbstractUser):
#     phone = models.CharField(
#         max_length=13,
#         blank=True,
#         validators=[phone_validator]
#     )

from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models

phone_validator = RegexValidator(
    regex=r'^\+375(25|29|33|44)\d{7}$',
    message="Введите номер в формате +375447410212"
)

class User(AbstractUser):
    phone = models.CharField(
        max_length=13,
        blank=True,
        validators=[phone_validator]
    )

    def __str__(self):
        return self.username
