from ursina import *
from animations import load_animation

class Player(Entity):
    def __init__(self, position=(0, -5), ground=None):
        super().__init__(
            model='quad',
            texture=load_animation('idle')[1],
            scale=(6, 6),
            position=position,
            origin_y=-0.2,
            collider='box',
        )

        # إعدادات الفيزياء
        self.gravity = -5.81
        self.velocity_y = 0
        self.is_jumping = False
        self.speed = 5
        self.ground = ground

        # متغيرات الأنيميشن
        self.current_state = 'idle'
        self.frame_index = 0
        self.frame_timer = 0.2
        self.frame_elapsed = 0
        self.last_direction = 'right'

        # متغيرات الضغط على الأزرار
        self.right_held = False
        self.left_held = False

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.velocity_y = 1.5
            self.current_state = 'jump' if self.last_direction == 'right' else 'jump_left'
            self.texture = load_animation(self.current_state)[0]
            self.frame_index = 0
            self.frame_elapsed = 0

    def update(self):
        moving = False

        # الحركة
        if held_keys['d'] or held_keys['right'] or self.right_held:
            self.x += self.speed * time.dt
            self.current_state = 'run'
            moving = True
            self.last_direction = 'right'

        elif held_keys['a'] or held_keys['left'] or self.left_held:
            self.x -= self.speed * time.dt
            self.current_state = 'run_left'
            moving = True
            self.last_direction = 'left'

        elif self.is_jumping:
            self.current_state = 'jump_left' if self.last_direction == 'left' else 'jump'
        else:
            self.current_state = 'idle_left' if self.last_direction == 'left' else 'idle'

        # سرعة الأنيميشن
        self.frame_timer = 0.5 if self.current_state in ['idle', 'idle_left', 'jump', 'jump_left'] else 0.1

        # عرض الإطارات
        frames = load_animation(self.current_state)
        if self.current_state in ['idle', 'idle_left', 'jump', 'jump_left']:
            if moving:
                self.texture = frames[self.frame_index]
            else:
                self.frame_index = 0
                self.frame_elapsed = 0
                self.texture = frames[0]
        else:
            self.texture = frames[self.frame_index]

        self.frame_elapsed += time.dt
        if self.frame_elapsed >= self.frame_timer:
            self.frame_index = (self.frame_index + 1) % len(frames)
            self.texture = frames[self.frame_index]
            self.frame_elapsed = 0

        # الجاذبية والقفز
        if self.is_jumping:
            self.velocity_y += self.gravity * time.dt
            self.y += self.velocity_y

        # حدود الشاشة
        min_x = -window.size[1] / 65
        max_x = window.size[1] / 65
        self.x = max(min(self.x, max_x), min_x)

    def check_ground_collision(self):
        if self.ground:
            ground_top = self.ground.y + self.ground.scale_y / 2
            player_bottom = self.y - self.scale_y / 2

            if player_bottom <= ground_top and self.velocity_y < 0:
                self.y = ground_top + self.scale_y / 2
                self.is_jumping = False
                self.velocity_y = 0

    def hold_right(self):
        self.right_held = True

    def release_right(self):
        self.right_held = False

    def hold_left(self):
        self.left_held = True

    def release_left(self):
        self.left_held = False