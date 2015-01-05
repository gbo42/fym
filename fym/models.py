from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class Usuario(models.Model):
    user = models.OneToOneField(User)

    apelido = models.CharField(max_length=30, unique=True)

    def __unicode__(self):
        return self.user.username

class Trilha(models.Model):
    name = models.CharField(max_length=128, unique=True)
    slug = models.SlugField(unique=True)
    likes = models.IntegerField(default=0)

    def get_first(self):
        bloco = Bloco.objects.filter(trilha = self.id)
        try:
            return bloco[0]
        except IndexError:
            return 'Ninguem comecou esta historia ainda.'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Trilha, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

class Bloco(models.Model):
    trilha = models.ForeignKey(Trilha)
    usuario = models.ForeignKey(User)
    texto = models.CharField(max_length=2000, unique=True)
    hearts = models.IntegerField(default=0)

    def get_track(self):
        trilha_ = Trilha.objects.get(name=self.trilha)
        return trilha_
    def __unicode__(self):
        return self.texto