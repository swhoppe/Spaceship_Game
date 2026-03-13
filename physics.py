import numpy as np
import math
from groups import *

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

### move_packs ###

class MovePack:
    def __init__(self):
        pass

    def update(self, dt):
        pass

class Impulse(MovePack):
    def __init__(self, vector, magnitude):
        super().__init__()
        self.transient = True
        self.active = True
        self.vector = vector * magnitude
    
    def update(self, dt):
        output = self.vector
        self.vector = self.vector * (0.85**(dt*60)) # decay by multiple of 0.85 every 1/60th of a second
        if np.linalg.norm(self.vector) < 0.0001:
            self.active = False
        return output
    
def apply_move_pack(move_pack, target):
    target.move_packs.append(move_pack)    

class Recoil:
    def __init__(self, vector, magnitude):
        self.vector = vector
        self.magnitude = magnitude
    
    def apply(self, target):
        apply_move_pack(Impulse(self.vector, self.magnitude), target)

class Impact:
    def __init__(self, range, magnitude):
        self.range = range
        self.magnitude = magnitude

    def apply(self, position, target):
        vector = np.array(target.rect.center) - np.array(position)
        norm = np.linalg.norm(vector) 
        vector = vector / norm
        if norm < self.range:
            apply_move_pack(Impulse(vector, self.magnitude), target)