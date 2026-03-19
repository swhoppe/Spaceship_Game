import numpy as np
import math
from groups import *
from entities import *
from utils import *

class MovePattern:
    def __init__(self):
        self.directed = False

    def init_state(self, obj):
        pass

    def __call__(self, obj):
        NotImplementedError     

class SinePattern(MovePattern):
    def __init__(self, amplitude, rate):
        super().__init__()
        self.amplitude = amplitude
        self.rate = rate

    def __call__(self, obj):
        return np.array([obj.speed, (self.amplitude * math.sin((obj.tof * self.rate)+math.pi/2))])

class ConstX(MovePattern):
    def __init__(self):
        super().__init__()

    def __call__(self, obj):
        return np.array([obj.speed, 0])
    
class TrackParent(MovePattern):
    def __init__(self):
        super().__init__()

    def init_state(self, obj):
        obj.last_y_pos = obj.parent.rect.y
    
    def __call__(self, obj):
        delta_y = obj.parent.rect.y - obj.last_y_pos
        obj.last_y_pos = obj.parent.rect.y
        return np.array([obj.speed, delta_y*60])
    
class GuidedMissile(MovePattern):
    def __init__(self):
        super().__init__()
        self.directed = True

    def __call__(self, obj):
        if enemies:
            vectors = np.empty((len(enemies), 2))
            for i, enemy in enumerate(enemies):
                vectors[i] = np.array(enemy.rect.center) - np.array(obj.rect.center)
            norms = np.linalg.norm(vectors, axis=1)
            min_index = np.argmin(norms)
            target_vector = vectors[min_index]
            target_norm = np.linalg.norm(target_vector) + 0.00001 # to avoid div by 0
            normed_target = target_vector / target_norm
            return normed_target * obj.speed
        else:
            return np.array([obj.speed, 0])
    
sine_pattern = SinePattern(5, 2)
gentle_sine = SinePattern(2, 2)
crazy_sine = SinePattern(8, 3)
constX = ConstX()
track_parent = TrackParent()
guided_missile = GuidedMissile()

### move_packs ###

class MovePack:
    def __init__(self):
        self.active = True
        self.tof = 0
        self.parent = None

    def update(self, dt):
        self.tof += dt

class Impulse(MovePack):
    def __init__(self, vector, magnitude):
        super().__init__()
        self.vector = vector * magnitude
    
    def update(self, dt):
        output = self.vector.astype(float) * ((100 / self.parent.max_hp)**0.5)
        self.vector = self.vector * (0.85**(dt*60)) # decay by multiple of 0.85 every 1/60th of a second
        if np.linalg.norm(self.vector) < 0.0001:
            self.active = False
        return output
    
class Park(MovePack):
    def __init__(self, x_pos):
        super().__init__()
        self.x_pos = x_pos

    def update(self, dt):
        if self.parent.rect.x >= self.x_pos:
            return constX(self.parent)
        else:
            self.active = False
            return np.zeros(2)
        
class DelayedPattern(MovePack):
    def __init__(self, pattern, delay):
        super().__init__()
        self.pattern = pattern
        self.delay = delay

    def update(self, dt):
        self.tof += dt
        if self.tof < self.delay:
            return np.zeros(2)
        else:
            return constX(self.parent)
        
class AvoidProjectile(MovePack):
    def __init__(self, radius, speed):
        super().__init__()
        self.radius = radius
        self.speed = speed
    
    def update(self, dt):
        vector = np.zeros(2)
        for projectile in projectiles:
            if isinstance(projectile.parent, Player):
                to_self = np.array(self.parent.rect.center) - np.array(projectile.rect.center)
                distance = np.linalg.norm(to_self)
                to_self_normed = to_self / (distance + 0.0001)
                if distance <= self.radius:
                    proj_vel_normed = projectile.velocity/(np.linalg.norm(projectile.velocity)+0.0001)
                    motivation = max(0, np.dot(to_self_normed, proj_vel_normed))
                    flee_vector = to_self_normed - np.dot(to_self_normed, proj_vel_normed)*proj_vel_normed
                    flee_norm = np.linalg.norm(flee_vector)
                    if flee_norm > 0.001:
                        flee_vector_normed = flee_vector / (flee_norm + 0.00001)
                    else:
                        flee_vector_normed = np.array([-proj_vel_normed[1], proj_vel_normed[0]])
                    proximity_scale = 1 - distance / self.radius
                    vector += flee_vector_normed * motivation * proximity_scale
        output = vector / (np.linalg.norm(vector)+0.00001) * self.speed
        if np.linalg.norm(output) > 0.01:
            print(output)
        return output

# MovePack Appliers    

def apply_move_pack(move_pack, target):
    move_pack.parent = target
    target.move_packs.append(move_pack)    

class Recoil:
    def __init__(self, vector, magnitude):
        self.vector = vector
        self.magnitude = magnitude
    
    def apply(self, target):
        apply_move_pack(Impulse(self.vector, self.magnitude), target)

class Impact:
    def __init__(self, radius, magnitude):
        self.radius = radius
        self.magnitude = magnitude

    def apply(self, position, target, damage):
        vector = np.array(target.rect.center) - np.array(position)
        distance = np.linalg.norm(vector)
        if distance < 0.0001:
            return
        else:
            if distance < self.radius:
                vector = vector / distance
                scaled_mag = self.magnitude*((1-distance/self.radius)**0.5)
                apply_move_pack(Impulse(vector, scaled_mag), target)
                if hasattr(target, 'hp'):
                    target.hp -= damage*((1-distance/self.radius)**0.5)
    
    def detonate(self, position, target):
        vector = np.array(target.rect.center) - np.array(position)
        distance = np.linalg.norm(vector)
        if distance < self.radius:
            target.hit()
