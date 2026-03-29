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
        return np.array([-obj.speed, (self.amplitude * math.sin((obj.tof * self.rate)+math.pi/2))])

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
const_up = Constant((0, -1))
const_down = Constant((0, 1))
track_parent = TrackParent()
guided_missile = GuidedMissile()

### move_packs ###

def _as_set(value):
    if value is None:
        return set()
    if isinstance(value, int):
        return {value}
    return set(value)

class MovePack:
    def __init__(self, active=True, expires_on_complete=False):
        self.active = active
        self.expired = False
        self.tof = 0
        self.parent = None
        self.activates_on = None
        self.deactivates_on = None
        self.emits = None
        self.expires_on_complete = expires_on_complete
        self.output = np.zeros(2)

    def update(self, dt):
        self.tof += dt
    
    def read_signal(self, signal):
        if self.activates_on is not None:
            if signal in self.activates_on:
                self.activate()
        if self.deactivates_on is not None:
            if signal in self.deactivates_on:
                self.deactivate()

    def activate(self):
        self.active = True

    def deactivate(self):
        self.active = False
    
    def complete(self):
        self.output = np.zeros(2)
        if self.expires_on_complete:
            self.expired = True
        self.active = False
        if self.emits is not None:
            self.parent.move_signals.update(self.emits)
            print(f'added emitted signal of {self.emits} to parent')

class Impulse(MovePack):
    def __init__(self, vector, magnitude, expires_on_complete=True):
        super().__init__(expires_on_complete=expires_on_complete)
        self.vector = vector * magnitude
    
    def update(self, dt):
        self.output = self.vector.astype(float) * ((100 / self.parent.max_hp)**0.5)
        self.vector = self.vector * (0.85**(dt*60)) # decay by multiple of 0.85 every 1/60th of a second
        if np.linalg.norm(self.vector) < 0.0001:
            self.complete()
    
class Delay(MovePack):
    def __init__(self, delay, emits, active=False, expires_on_complete=True):
        super().__init__(active, expires_on_complete=expires_on_complete)
        self.delay = delay
        self.emits = _as_set(emits)
        self.output = np.zeros(2)
    
    def update(self, dt):
        self.tof += dt
        if self.tof >= self.delay:
            print('delay completed')
            self.complete()

class MoveLeftTo(MovePack):
    def __init__(self, x_stop, activates_on, deactivates_on, emits, active=True):
        super().__init__(active)
        self.x_stop = x_stop
        self.activates_on = _as_set(activates_on)
        self.deactivates_on = _as_set(deactivates_on)
        self.emits = _as_set(emits)

    def update(self, dt):
        if self.parent.rect.left > self.x_stop:
            self.output = const_left(self.parent)
        else:
            self.complete()

class MoveRightTo(MovePack):
    def __init__(self, x_stop, activates_on, deactivates_on, emits, active=True):
        super().__init__(active)
        self.x_stop = x_stop
        self.activates_on = _as_set(activates_on)
        self.deactivates_on = _as_set(deactivates_on)
        self.emits = _as_set(emits)

    def update(self, dt):
        if self.parent.rect.right < self.x_stop:
            self.output = const_right(self.parent)
        else:
            self.complete()

class MoveUpTo(MovePack):
    def __init__(self, y_stop, activates_on, deactivates_on, emits, active=True):
        super().__init__(active)
        self.y_stop = y_stop
        self.activates_on = _as_set(activates_on)
        self.deactivates_on = _as_set(deactivates_on)
        self.emits = _as_set(emits)

    def update(self, dt):
        if self.parent.rect.top > self.y_stop:
            self.output = const_up(self.parent)
        else:
            self.complete()

class MoveDownTo(MovePack):
    def __init__(self, y_stop, activates_on, deactivates_on, emits, active=True):
        super().__init__(active)
        self.y_stop = y_stop
        self.activates_on = _as_set(activates_on)
        self.deactivates_on = _as_set(deactivates_on)
        self.emits = _as_set(emits)

    def update(self, dt):
        if self.parent.rect.bottom < self.y_stop:
            self.output = const_down(self.parent)
        else:
            self.complete()

class MoveLeftFor(MovePack):
    def __init__(self, x_dist, activates_on, deactivates_on, emits, active=True):
        super().__init__(active)
        self.x_dist = x_dist
        self.activates_on = _as_set(activates_on)
        self.deactivates_on = _as_set(deactivates_on)
        self.emits = _as_set(emits)
        self.start_x = 0.0

    def update(self, dt):
        if self.parent.rect.left > self.start_x - self.x_dist:
            self.output = const_left(self.parent)
        else:
            self.complete()
    
    def activate(self):
        self.start_x = self.parent.rect.left
        self.active = True

# enemy movement programs
def back_and_forth():
    return [MoveLeftTo((GAME_WIDTH/3), 0, None, 1),
            MoveRightTo((2*GAME_WIDTH/3), 1, None, 0, active=False)]
def square_path():
    return [
    MoveLeftTo(600, 0, None, 1),
    MoveDownTo(600, 1, None, 2, active=False),
    MoveRightTo(900, 2, None, 3, active=False),
    MoveUpTo(200, 3, None, 0, active=False)]

def caterpillar_movement(delay):
    return [
        Delay(delay, 0, active=True),
        MoveLeftTo(GAME_WIDTH-100, 0, 9, 1, active=False),
        MoveUpTo(0, 1, 9, 2, active=False),
        MoveLeftFor(128, 2, 9, 3, active=False),
        MoveDownTo(GAME_HEIGHT, 3, 9, 4, active=False),
        MoveLeftFor(128, 4, 9, 1, active=False),
        HitSignal(None, 9, active=True),
        SeekNearestPlayer(9, None, active=False)
        ]
            
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
    def __init__(self, activates_on, deactivates_on, active=True):
        super().__init__(active)
        self.activates_on = _as_set(activates_on)
        self.deactivates_on = _as_set(deactivates_on)

    def update(self, dt):
        if not players['active']:
            self.output = np.zeros(2)
        else:
            vectors = {player: np.array(player.rect.center) - np.array(self.parent.rect.center)
                    for player in players['active']}
            closest_player = min(vectors, key=lambda p: np.linalg.norm(vectors[p]))
            to_closest = vectors[closest_player]
            to_closest_normed = to_closest / (np.linalg.norm(to_closest) + 0.0001)
            self.output = to_closest_normed * self.parent.speed

class HitSignal(MovePack):
    def __init__(self, activates_on, emits, active=True, expires_on_complete=True):
        super().__init__(active, expires_on_complete=expires_on_complete)
        self.activates_on = _as_set(activates_on)
        self.emits = _as_set(emits)
    
    def update(self, dt):
        self.output = np.zeros(2)
        if self.parent.hp < self.parent.max_hp:
            self.complete()

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
