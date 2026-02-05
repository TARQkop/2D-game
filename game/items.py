from ursina import *
import random
import os

class Apple(Entity):
    def __init__(self, position, score_ref, score_text_ref):
        # الحصول على مسار المجلد الأساسي
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)

        super().__init__(
            model='quad',
            texture='../The structures are collapsing/Apple.png',
            scale=(1, 1),
            position=position,
            collider='box'
        )
        self.fall_speed = 0.03
        self.score_ref = score_ref
        self.score_text_ref = score_text_ref
        self.player = None  # سيتم تعيينه لاحقاً

    def set_player(self, player):
        self.player = player

    def update(self):
        self.y -= self.fall_speed

        if self.player:
            # حساب المسافة بين التفاحة واللاعب
            distance = distance_2d(self.position, self.player.position)

            # عند جمع التفاحة
            if distance < 1.5:
                destroy(self)
                self.score_ref[0] += 1
                self.score_text_ref.text = f"Points: {self.score_ref[0]}"
                print('apple collected! 🍎')

        # حذف التفاحة إن سقطت تحت الشاشة
        elif self.y < -10:
            destroy(self)

class Explosion(Entity):
    def __init__(self, position, images, scale=1.5, frame_duration=0.05):
        super().__init__(
            model='quad',
            texture=images[0],
            position=position,
            scale=scale,
            billboard=True
        )
        self.images = images
        self.frame_duration = frame_duration
        self.frame_index = 0
        self.time_since_last_frame = 0

    def update(self):
        self.time_since_last_frame += time.dt
        if self.time_since_last_frame >= self.frame_duration:
            self.time_since_last_frame = 0
            self.frame_index += 1
            if self.frame_index < len(self.images):
                self.texture = self.images[self.frame_index]
            else:
                destroy(self)

class Bomb(Entity):
    def __init__(self, position, player, lose_heart_callback):
        # الحصول على مسار المجلد الأساسي
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)

        super().__init__(
            model='quad',
            texture='../The structures are collapsing/BOOMB.png',
            scale=(0.95, 0.95),
            position=position,
            collider='box'
        )
        self.speed = 0.035
        self.rotation_speed = random.uniform(-4, 4)
        self.player = player
        self.collected = False
        self.lose_heart_callback = lose_heart_callback

    def update(self):
        self.y -= self.speed
        self.rotation_z += self.rotation_speed

        distance = distance_2d(self.position, self.player.position)

        if distance < 1.5 and not self.collected:
            self.collected = True
            explosion_pos = self.position
            destroy(self)
            print('💣 boom 1- you lost a heart!')
            self.lose_heart_callback()

            # الحصول على مسار المجلد الأساسي للانفجار
            current_dir = os.path.dirname(os.path.abspath(__file__))
            parent_dir = os.path.dirname(current_dir)
            images = [f'../explosions/boom/boom_{i}.png' for i in range(29)]
            Explosion(position=explosion_pos, images=images, scale=2)

            for _ in range(4):
                self.player.position += Vec3(
                    random.uniform(-0.1, 0.1),
                    random.uniform(-0.1, 0.1),
                    0
                )
            invoke(setattr, self.player, 'position', self.player.position, delay=0.05)