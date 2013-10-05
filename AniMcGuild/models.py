from django.db import models

# Create your models here.



class HeroClass(models.Model):
    name = models.CharField(max_length=30)
    hp_bonus = models.IntegerField()
    ac_bonus = models.IntegerField()
    ref_bonus = models.IntegerField()
    

class Skills(models.Model):
    ATTACK_TYPES = (
        ('ME', "Melee"),
        ('RN', "Ranged"),
    )
    name = models.CharField(max_length=30)
    attack_type = models.CharField(max_length=2, choices=ATTACK_TYPES)
    hit = models.CharField(max_length=30)
    silences = models.BooleanField(default=False)

class Hero(models.Model):
    hero_class = models.ForeignKey(HeroClass)
