import numpy as np
import rpg_utils
from rpg_utils import sum_highest_3_of_4d6
import races, armor, weapons, char_classes
from collections import Counter
from DnD4py import lookup_5e
import re


# Define string shortcuts for stats as used in DnD
STATS = ['str', 'dex', 'con', 'int', 'wis', 'cha']

class Entity:
    """
    Base class providing name, stats, and level.
    """

    def __init__(self,
                 name: str,
                 stats: dict = None,
                 level: int = 1,
                 race: str = 'human',
                 char_class: str = 'fighter',
                 weapon: str = 'unarmed',
                 armor: str = 'none'):
        # Initialise name, level and base stats
        # HP come with class due to hit dice
        # TODO: test stats list for length/validity/type being Counter
        # TODO: test name for uniqueness
        # TODO: test name for existence in Monster manual and if, autofill stats etc
        # TODO: add option for Versatile weapons to use dex modifier for attack/dmg
        # TODO: add saving throw option for poisons etc

        self.name = name
        self.level = level
        if not stats:
            self.stats = Counter({stat: sum_highest_3_of_4d6() for stat in STATS})

        else:
            self.stats = stats

        # Look up racial modifiers and apply
        racial_modifiers = getattr(races, '{}'.format(race))
        self.stats.update(Counter(racial_modifiers))

        # Get modifier for each stat
        self.check_modifiers = {stat: rpg_utils.get_modifier(self.stats[stat]) for stat in STATS}

        # Apply character class
        char_class_profile = getattr(char_classes, '{}'.format(char_class))
        self.determine_hit_points(char_class_profile)

        # TODO: postpone attack modifier definition until after weapon, consider Finesse
        # TODO: check for Weapon after Armor to check for shield
        # TODO: add armor lookup
        self.attack_modifier = self.check_modifiers['str']

        self.Armor = Armor(name=armor, dex_modifier=self.check_modifiers['dex'])
        self.armor_class = self.Armor.ac

        # TODO: add weapon lookup
        self.Weapon = Weapon(name=weapon)
    def calculate_damage(self, weapon, attack_modifier, critical: bool=False):
        """
        Calculate damage from attack and modify hp
        Args:
            weapon: obj, instance of weapon used by attacker
            attack_modifier: attacker's damage bonus/malus
            critical: Whether attack was critical hit

        """
        if not critical:
            damage = weapon.damage() + attack_modifier
        else:
            damage = weapon.damage() + weapon.damage() + attack_modifier

        self.hp = self.hp - damage

    def determine_hit_die_roller(self, char_class_profile):
        """
        Determines hit points based on level.
        Args:
            char_class:

        Returns:

        """
        # Find hit die in class description and turn into integer
        hit_die = char_class_profile['hit_die']
        hit_die = re.findall('(?<=d)[0-9]+', hit_die)[0]
        hit_die_roller = getattr(rpg_utils, 'roll_d{}'.format(hit_die))

        return hit_d


        # Set base hit points
        self.hp = int(hit_die) + self.check_modifiers['con']

        # Get hit points for levels above 1
        for i in range(self.level - 1):
            level_hit_points = hit_die_roller() + self.check_modifiers['con']
            self.hp += level_hit_points




class Weapon:
    """
    Class for weapon instances
    """
    # TODO: Add check for proper damage string format
    def __init__(self, name: str = 'unarmed'):
        weapon_profile = getattr(weapons, name)
        self.name = name
        self.damage = self.determine_damage_fctn(weapon_profile['damage'])
        self.dmg_type = weapon_profile['damage_type']

    def determine_damage_fctn(self, damage: str):
        """
        Create function to roll weapon damage
        Args:
            damage: string in format 'xdxx' e.g. '1d6'

        Returns:
            function that will roll as many of the specified dice as given
        """
        num_dice, type_die = [int(x) for x in damage.split('d')]
        if type_die > 1:
            die_roller = getattr(rpg_utils, "roll_d{}".format(type_die))
        else:
            def die_roller():
                return 1
        def damage_roller():
            dmg = 0
            for i in range(num_dice):
                new_dmg = die_roller()
                dmg += new_dmg
            return dmg

        return damage_roller

class Armor:
    """
    Class for armor instances
    """
    # TODO: All sorts of stuff... immunities etc
    # TODO: Work out combinations, e.g. hauberk + shield etc

    def __init__(self, name: str = 'none', ac: int = 10, dex_modifier: int = 0):
        self.name = name
        self.ac = ac + dex_modifier
