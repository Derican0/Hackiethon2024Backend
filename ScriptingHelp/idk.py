# bot code goes here
from Game.Skills import *
from Game.projectiles import *
from ScriptingHelp.usefulFunctions import *
from Game.playerActions import defense_actions, attack_actions, projectile_actions
from gameSettings import HP, LEFTBORDER, RIGHTBORDER, LEFTSTART, RIGHTSTART, PARRYSTUN


# PRIMARY CAN BE: Teleport, Super Saiyan, Meditate, Dash Attack, Uppercut, One Punch
# SECONDARY CAN BE : Hadoken, Grenade, Boomerang, Bear Trap

# TODO FOR PARTICIPANT: Set primary and secondary skill here
PRIMARY_SKILL = TeleportSkill
SECONDARY_SKILL = Hadoken

#constants, for easier move return
#movements
JUMP = ("move", (0,1))
FORWARD = ("move", (1,0))
BACK = ("move", (-1,0))
JUMP_FORWARD = ("move", (1,1))
JUMP_BACKWARD = ("move", (-1, 1))

# attacks and block
LIGHT = ("light",)
HEAVY = ("heavy",)
BLOCK = ("block",)

PRIMARY = get_skill(PRIMARY_SKILL)
SECONDARY = get_skill(SECONDARY_SKILL)

# no move, aka no input
NOMOVE = "NoMove"
# for testing
moves = SECONDARY,
moves_iter = iter(moves)

# TODO FOR PARTICIPANT: WRITE YOUR WINNING BOT
class Script:
    def __init__(self):
        self.primary = PRIMARY_SKILL
        self.secondary = SECONDARY_SKILL
        
    # DO NOT TOUCH
    def init_player_skills(self):
        return self.primary, self.secondary
    
    # MAIN FUNCTION that returns a single move to the game manager
    def get_move(self, player, enemy, player_projectiles, enemy_projectiles):

        # STATE MACHINE!! ATTACK or DEFEND MODE

        # ATTACK and DEFENCE is based on player/enemy cooldown
        
        # ATTACK 1 (GRENADE COOLDOWN)
            # CHECK DISTANCE AND IF DISTANCE IS 3, THROW GRENADE
            # ELSE: MOVE
        
        # ATTACK 2 (ENEMY ON COOLDOWN) DASH ATTACK TOWARDS ENEMY AND COMBO
        
        #DEFEND (WE ON COOL DOWN)
            # BLOCK IF PROJECTILE IS DETECTED
            # JUMP AWAY FROM ENEMY

        # GRENADE!
        if not secondary_on_cooldown(player):
            return SECONDARY
        
        # BLOCK
        if len(enemy_projectiles) > 0:
            proj_distance = (abs(get_pos(player)[0] - (get_proj_pos(enemy_projectiles[0])[0])))
            if proj_distance < 2:
                return BLOCK
        
        # LIGHT
        distance = abs(get_pos(player)[0] - get_pos(enemy)[0])
        if distance < 3:
            return LIGHT
        
        return FORWARD
