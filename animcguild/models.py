from django.db import models
from animcguild.functions import roll
# Create your models here.



class HeroClass(models.Model):
    name = models.CharField(max_length=30)
    hp_bonus = models.IntegerField()
    ac_bonus = models.IntegerField()
    ref_bonus = models.IntegerField()
    weapon_score = models.IntegerField()
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
    strength = models.IntegerField(default=10)
    dexterity = models.IntegerField(default=10)
    constitution = models.IntegerField(default=10)
    wisdom = models.IntegerField(default=10)
    skill_points = models.IntegerField(default=12)
    taunter = models.ForeignKey('self', null = True, blank = True)
    inititive = models.IntegerField(default=0)
    level = models.IntegerField(default=1)
    hp = models.IntegerField(default=0)
    targetable = models.BooleanField(default = True)
    silent = models.BooleanField(default = False)
    used_ultimate = models.BooleanField(default = False)
    used_utilities = models.ManyToManyField(Skills)
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
    def str_mod(self):
        return (self.strength / 2) - 5
    def wis_mod(self):
        return (self.wisdom / 2) - 5
    def con_mod(self):
        return (self.constitution / 2) - 5
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
    def lvl_up(self):
        self.skill_points += 2
        self.level += 1
        self.save()
    def use_ability(self, ability, target):
        STRMOD = self.str_mod()
        DEXMOD = self.dex_mod()
        WIS = self.wisdom
        
class Modifier(models.Model):
    hero = models.ForeignKey(Hero)
    STATS = (
        ('STR', "Strength"),
        ('DEX', "Dexterity"),
        ('WIS', "Wisdom"),
        ('CON', "Constitution"),
    )
    stat = models.CharField(max_length=3, choices=STATS)
    mod = models.IntegerField()
    def apply_str(self,val):
        self.hero.strength += val
    def apply_dex(self,val):
        self.hero.dexterity += val
    def apply_wis(self,val):
        self.hero.wisdom += val
    def apply_con(self,val):
        self.hero.constitution += val

    ACTION = {
        'STR':apply_str,
        'DEX':apply_dex,
        'WIS':apply_wis,
        'CON':apply_con,
    }

    def apply_mod(self):
        ACTION[self.stat](self.mod)
    def end_mod(self):
        ACTION[self.stat](-self.mod)
