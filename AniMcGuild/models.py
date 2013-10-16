from django.db import models
from AniMcGill.functions import roll
# Create your models here.



class HeroClass(models.Model):
    name = models.CharField(max_length=30)
    hp_bonus = models.IntegerField()
    ac_bonus = models.IntegerField()
    ref_bonus = models.IntegerField()
    def __unicode__(self):
        return self.name
    

class Skills(models.Model):
    ATTACK_TYPES = (
        ('ME', "Melee"),
        ('RN', "Ranged"),
    )
    name = models.CharField(max_length=30)
    attack_type = models.CharField(max_length=2, choices=ATTACK_TYPES)
    damage = models.CharField(max_length=255)
    ultimate = models.BooleanField(default=False)
    utility = models.BooleanField(default=False)
    silences = models.BooleanField(default=False)
    def __unicode__(self):
        return self.name

class Hero(models.Model):
    hero_class = models.ForeignKey(HeroClass)
    name = models.CharField(max_length = 255)
    strength = models.IntegerField()
    dexterity = models.IntegerField()
    constitution = models.IntegerField()
    wisdom = models.IntegerField()
    taunter = models.ForeignKey(Hero, empty = True, blank = True)
    inititive = models.IntegerField()
    level = models.IntegerField()
    hp = models.IntegerField()
    targetable = models.BooleanField(default = True)
    silent = models.BooleanField(default = False)
    used_ultimate = models.BooleanField(default = False)
    def __unicode__(self):
        return self.name
    def reflex(self):
        return 10 + (self.level / 2) + self.hero_class.ref_bonus
    def ac(self):
        return 10 + (self.level / 2) + self.hero_class.ac_bonus
    def max_hp(self):
        return self.constitution + (self.level / 2) + self.hero_class.hp_bonus
    def dex_mod(self):
        return (self.dexterity / 2) - 5
    def roll_init(self):
        self.inititive = self.dex_mod() + (self.level / 2) + roll(1,20)
        self.save()
    def reset(self):
        self.hp = self.max_hp()
        self.taunter = None
        self.silent = False
        self.inititive = 0
        self.used_ultimate = False
        self.save()
