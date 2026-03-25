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

class Constant(MovePattern):
    def __init__(self, direction):
        super().__init__()
        self.vector = np.array(direction)

    def __call__(self, obj):
        return np.array(self.vector) * obj.speed
    
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
const_left = Constant((-1, 0))
const_right = Constant((1, 0))
track_parent = TrackParent()
guided_missile = GuidedMissile()

### move_packs ###

class MovePack:
    def __init__(self, active=True):
        self.active = active
        self.complete = False
        self.tof = 0
        self.parent = None
        self.to_start = None
        self.to_stop = None
        self.on_stop = None
        self.output = None

    def update(self, dt):
        self.tof += dt
    
    def read_signal(self, signal):
        if self.to_start is not None:
            if self.to_start == signal:
                self.start()
        if self.to_stop is not None:
            if self.to_stop == signal:
                self.stop()

    def start(self):
        self.active = True
    
    def stop(self):
        self.active = False
        if self.on_stop is not None:
            self.parent.move_signals.add(self.on_stop)
            print(f'added on_stop signal of {self.on_stop} to parent')

class Impulse(MovePack):
    def __init__(self, vector, magnitude):
        super().__init__()
        self.vector = vector * magnitude
    
    def update(self, dt):
        self.output = self.vector.astype(float) * ((100 / self.parent.max_hp)**0.5)
        self.vector = self.vector * (0.85**(dt*60)) # decay by multiple of 0.85 every 1/60th of a second
        if np.linalg.norm(self.vector) < 0.0001:
            self.stop()
    
class Delay(MovePack):
    def __init__(self, delay, on_stop, active=False):
        super().__init__(active)
        self.delay = delay
        self.on_stop = on_stop
        self.output = np.zeros(2)
    
    def update(self, dt):
        self.tof += dt
        if self.tof >= self.delay:
            self.stop()

five_s_delay = Delay(5, 0)

class MoveLeftTo(MovePack):
    def __init__(self, x_stop, to_start, on_stop, active=True):
        super().__init__(active)
        self.x_stop = x_stop
        self.to_start = to_start
        self.on_stop = on_stop
        self.last_pos = None

    def update(self, dt):
        # print(self.parent.rect.center)
        if self.parent.rect.left > self.x_stop:
            self.output = const_left(self.parent)
        else:
            self.stop()

class MoveRightTo(MovePack):
    def __init__(self, x_stop, to_start, on_stop, active=True):
        super().__init__(active)
        self.x_stop = x_stop
        self.to_start = to_start
        self.on_stop = on_stop
        self.last_pos = None

    def update(self, dt):
        # print(self.parent.rect.center)
        if self.parent.rect.left < self.x_stop:
            self.output = const_right(self.parent)
        else:
            self.stop()

back_and_forth = [MoveLeftTo((GAME_WIDTH/3), 0, 1), MoveRightTo((2*GAME_WIDTH/3), 1, 0, active=False)]
    
class Park(MovePack):
    def __init__(self, x_pos):
        super().__init__()
        self.x_pos = x_pos

    def update(self, dt):
        if self.parent.rect.x >= self.x_pos:
            self.output = const_left(self.parent)
        else:
            self.complete = False
            self.output = np.zeros(2)
        
class DelayedPattern(MovePack): # uses a MovePattern objects __call__ after a given delay
    def __init__(self, pattern, delay):
        super().__init__()
        self.pattern = pattern
        self.delay = delay

    def update(self, dt):
        self.tof += dt
        if self.tof < self.delay:
            self.output = np.zeros(2)
        else:
            self.output = self.pattern(self.parent)
        
class Rush(MovePack):
    def __init__(self, delay):
        super().__init__()
        self.delay = delay
        self.move_dict = {'rush': const_left, 'retreat': const_right}
        self.status = 'idle'

    def update(self, dt):
        self.tof += dt
        if self.tof < self.delay:
            return np.zeros(2)
        if self.status ==  'idle' and self.tof >= self.delay:
            self.status = 'rush'
            return self.move_dict[self.status](self.parent)
        if self.status == 'rush' and self.parent.rect.left > 100:
            return self.move_dict[self.status](self.parent)
        if self.status == 'rush' and self.parent.rect.left <= 100:
            self.status = 'retreat'
            return self.move_dict[self.status](self.parent)
        if self.status == 'retreat' and self.parent.rect.right < GAME_WIDTH - 150:
            return self.move_dict[self.status](self.parent)
        if self.status == 'retreat' and self.parent.rect.right >= GAME_WIDTH - 150:
            self.status = 'complete'
            return np.zeros(2)
        if self.status == 'complete':
            self.active = False
            return np.zeros(2)
            
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
        self.output = vector / (np.linalg.norm(vector)+0.00001) * self.speed
    
class SeekNearestPlayer(MovePack):
    def __init__(self):
        super().__init__()

    def update(self, dt):
        if not players['active']:
            self.output = np.zeros(2)
        vectors = {player: np.array(player.rect.center) - np.array(self.parent.rect.center)
                   for player in players['active']}
        closest_player = min(vectors, key=lambda p: np.linalg.norm(vectors[p]))
        to_closest = vectors[closest_player]
        to_closest_normed = to_closest / (np.linalg.norm(to_closest) + 0.0001)
        self.output = to_closest_normed * self.parent.speed

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
