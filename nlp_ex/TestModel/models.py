from django.db import models

# Create your models here.
class NLP(models.Model):
    name = models.CharField(max_length=20)

class UserInfo(models.Model):
    user_id = models.IntegerField(primary_key=True)
    user_name = models.CharField(max_length=30)
    pass_word = models.CharField(max_length=64)
    user_token = models.CharField(max_length=64)
    token_last_modified = models.DateTimeField()

    def __str__(self):
        return self.user_name