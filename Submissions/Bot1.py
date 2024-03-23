# bot code goes here
from Game.Skills import *
from Game.projectiles import *
from ScriptingHelp.usefulFunctions import *
from Game.playerActions import defense_actions, attack_actions, projectile_actions
from Game.gameSettings import HP, LEFTBORDER, RIGHTBORDER, LEFTSTART, RIGHTSTART, PARRYSTUN


# PRIMARY CAN BE: Teleport, Super Saiyan, Meditate, Dash Attack, Uppercut, One Punch
# SECONDARY CAN BE : Hadoken, Grenade, Boomerang, Bear Trap

# TODO FOR PARTICIPANT: Set primary and secondary skill here
PRIMARY_SKILL = DashAttackSkill
SECONDARY_SKILL = Grenade

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
CANCEL = ("skill_cancel", )

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
        self.comboList = [LIGHT, LIGHT, HEAVY]
        self.moves_used = []
        
    # DO NOT TOUCH
    def init_player_skills(self):
        return self.primary, self.secondary
    
    # MAIN FUNCTION that returns a single move to the game manager
    def get_move(self, player, enemy, player_projectiles, enemy_projectiles):
        distance = abs(get_pos(player)[0] - get_pos(enemy)[0])

        # AVOID WALL
        print(get_pos(player))
        if get_pos(player)[0] in [0, 15]:
            return PRIMARY

        # GRENADE STATE
        if not secondary_on_cooldown(player):
            if distance == 4:
                return SECONDARY
            elif distance > 4:
                return FORWARD
            elif distance < 4:
                return BACK
            
        # ATTACK STATE
        if get_secondary_cooldown(enemy) > 3 or get_primary_cooldown(enemy) > 3 or get_stun_duration(enemy) > 2:
            if not get_primary_cooldown(player) > 0:
                return PRIMARY
            return heavy_combo(player, enemy)
            
        # DEFEND STATE
        # BlOCKING PROJECTILES
        if len(enemy_projectiles) > 0:
            proj_distance = (abs(get_pos(player)[0] - (get_proj_pos(enemy_projectiles[0])[0])))
            if proj_distance < 2:
                return BLOCK
        # AVOID PLAYER
        if distance < 5:
            print(player.get_pos())
            return BACK
        
        return LIGHT