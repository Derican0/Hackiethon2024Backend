import itertools
from Skills import AttackSkill

class Projectile:
    # auto increment projectile id whenever a new projectile is summoned
    id = itertools.count()
    
    def __init__(self, player, path, size, type, trait, collision):
        # size = (x, y) hitbox size of projectile
        # type =  type of projectile eg hadoken
        self.xCoord = player._xCoord + path[0][0]
        self.yCoord = player._yCoord + path[0][1]
        self._direction = player._direction
        self.initdirection = self._direction
        self.distance = 0
        self.size = size
        self.type = type
        
        # True if projectile damages on hit during travel eg hadoken, lasso
        # False if prpojectile damages after travel eg ice wall, landmine
        self.collision = collision
        
        # trait = effect after projectile has travelled its path
        # pop = remove projectile, explode = AOE dmg after timer, timer = pop after timer, no dmg
        self.trait = trait
        self.id = next(self.id)
        self.player = player
        
        # this is an array of projectile positions relative to cast position over time
        self.path = path
        self.pathIndex = 0
        # initialize path acording to player direction, only change xCoord
        for i in range(len(self.path)):
            self.path[i][0] *= self._direction


    def travel(self):
        self.pathIndex += 1
        if self.pathIndex < len(self.path):
            pos = self.path[self.pathIndex]
            self.xCoord += pos[0] - self.path[self.pathIndex - 1][0]
            self.yCoord += pos[1] - self.path[self.pathIndex - 1][1]
        else:
            # has reached end of path, so do effects based on trait
            self.do_trait()
            
      
    def do_trait(self):
        if not self.trait:
            # pop
            self.size = (0, 0)
        elif self.trait == "return":
            # dynamically return towards player
            self._direction = -1 * self.initdirection
            if (self.xCoord == self.player._xCoord and 
                self.yCoord == self.player._yCoord):
                # boomerang caught, or player in front of projectile
                self.size = (0,0)
            elif (self.player._xCoord - self.xCoord) * self._direction > 0 :
                # if the player is currently at least behind the projectile 
                # travel towards caster
                self.xCoord += self._direction
                if self.yCoord < self.player._yCoord:
                    self.yCoord += 1
                elif self.yCoord > self.player._yCoord:
                    self.yCoord -= 1
            else:
                self.size = (0,0)
            pass
        elif self.trait == "timer":
            # stay at current position for given time to live
            pass
        elif self.trait == "timer_explode":
            # similar to timer, but does aoe damage after timer
            pass
        
           
    def get_pos(self):
        return (self.xCoord, self.yCoord)
            

    def checkCollision(self, target):
        # checks if projectile has a size
        if self.size[0] and self.size[1] and self.collision:
            # checks if projectile hits target
            if (abs(target._xCoord-self.xCoord) < self.size[0] and
                abs(target._yCoord-self.yCoord) < self.size[1]):
                return target != self.player
        return False
            
    def checkProjCollision(self, target):
        if self.size[0] and self.size[1]:
            if (abs(target.xCoord + target.size[0]*target._direction 
                    - self.xCoord) < self.size[0] and
                abs(target.yCoord + target.size[1]-self.yCoord) < self.size[1]):
                return True
        return False
    
class ProjectileSkill(AttackSkill):
    def __init__(self, player, startup, cooldown, damage, blockable, knockback,
                 stun, skillName):
        AttackSkill.__init__(self, startup=startup, cooldown=cooldown, 
                            damage=damage, xRange=0, vertical=0, 
                            blockable=blockable, knockback=knockback, 
                            stun=stun)
        self.player = player
        self.skillType = skillName
        
    def summonProjectile(self, path, size, trait, collision):
        projectile = Projectile(self.player, path, size, self.skillType, trait, collision)
        return projectile
    

class Hadoken(ProjectileSkill):
    def __init__(self, player):
        ProjectileSkill.__init__(self, player, startup=0, cooldown=10, damage=10,
                                 blockable=True, knockback=2, stun=2, 
                                 skillName="hadoken")
        self.path = [[1, 0], [2, 0], [3, 0], [4, 0], [5, 0]]
    
    def activateSkill(self):
        atk_info = super().activateSkill()
        if isinstance(atk_info, int):
            return atk_info
        
        projectile = self.summonProjectile(path = self.path, size=(1,1), 
                                           trait=None, collision=True)
        return [self.skillType,  {"damage":self.skillValue, "blockable": self.blockable, 
                "knockback":self.knockback, "stun":self.stun, 
                "projectile": projectile}]
    
    
class Lasso(ProjectileSkill):
    def __init__(self, player):
        ProjectileSkill.__init__(self, player, startup=0, cooldown=10, damage=5,
                                 blockable=True, knockback=-2, stun=0, 
                                 skillName="lasso")
        self.path = [[1, 0], [2, 0], [3, 0], [4, 0], [5, 0]]
    
    def activateSkill(self):
        atk_info = super().activateSkill()
        if isinstance(atk_info, int):
            return atk_info
        
        projectile = self.summonProjectile(path=self.path, size=(1,1), 
                                           trait=None, collision=True)
        return [self.skillType,  {"damage":self.skillValue, "blockable": self.blockable, 
                "knockback":self.knockback, "stun":self.stun, 
                "projectile": projectile}]
        
class Boomerang(ProjectileSkill):
    def __init__(self, player):
        ProjectileSkill.__init__(self, player, startup=0, cooldown=10, damage=5,
                                 blockable=True, knockback=2, stun=2, 
                                 skillName="boomerang")
        self.path = [[1, 0], [2, 0], [3, 0], [4, 0], [5, 0]]
    
    def activateSkill(self):
        atk_info = super().activateSkill()
        if isinstance(atk_info, int):
            return atk_info
        
        projectile = self.summonProjectile(path = self.path, size=(1,1), 
                                           trait="return", collision=True)
        return [self.skillType,  {"damage":self.skillValue, "blockable": self.blockable, 
                "knockback":self.knockback, "stun":self.stun, 
                "projectile": projectile}]