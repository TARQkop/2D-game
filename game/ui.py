from ursina import *
import os

class Heart(Entity):
    def __init__(self, position, scale=0.12, texture=None):
        # الحصول على مسار المجلد الأساسي
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)
        if texture is None:
            texture = '../The structures are collapsing/hart.png'

        super().__init__(
            model='quad',
            texture=texture,
            scale=(scale, scale),
            position=position,
            parent=camera.ui
        )
        self.original_scale = self.scale
        self.blinking = False
        self.shaking = False

    def blink(self, duration=0.2, times=3):
        """Blink when losing a heart."""
        if self.blinking:
            return
        self.blinking = True
        def do_blink():
            for _ in range(times):
                self.scale = (0, 0)
                invoke(setattr, self, 'scale', self.original_scale, delay=duration)
                yield duration*2
            self.blinking = False
        invoke(do_blink)

    def shake(self, intensity=0.05, duration=0.2):
        """Rapid heartbeat."""
        if self.shaking:
            return
        self.shaking = True
        original_pos = self.position
        def do_shake():
            for _ in range(int(duration*10)):
                self.x = original_pos[0] + random.uniform(-intensity,intensity)
                self.y = original_pos[1] + random.uniform(-intensity,intensity)
                yield 0.02
            self.position = original_pos
            self.shaking = False
        invoke(do_shake)

class UI:
    def __init__(self):
        # الحصول على مسار المجلد الأساسي
        current_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(current_dir)

        self.hearts = []
        self.max_hearts = 3
        self.score_text = Text(text="Points: 0", position=(-0.85, 0.45), scale=1.5, color=color.orange, parent=camera.ui)
        self.score_text.enabled = False

        # إنشاء القلوب
        for i in range(self.max_hearts):
            heart = Heart(position=Vec2(-0.8 + i * 0.12, 0.40))
            heart.enabled = False
            self.hearts.append(heart)

        # أزرار البداية
        self.start_button = Button(parent=camera.ui, model='quad', texture='../start/start.png', scale=(0.3, 0.1), position=(0, 0.1), color=color.white)
        self.settings_button = Button(parent=camera.ui, model='quad', texture='../start/settings.png', scale=(0.3, 0.1), position=(0, -0.05), color=color.white)
        self.exit_button = Button(parent=camera.ui, model='quad', texture='../start/exit.png', scale=(0.3, 0.1), position=(0, -0.2), color=color.white)

        # أزرار الحركة اللمسية
        self.right_btn = Button(parent=camera.ui, model='quad', texture='../start/→.png', scale=(0.15, 0.15), position=(-0.55, -0.3), color=color.white, enabled=False)
        self.left_btn = Button(parent=camera.ui, model='quad', texture='../start/←.png', scale=(0.15, 0.15), position=(-0.75, -0.3), color=color.white, enabled=False)
        self.jump_btn = Button(parent=camera.ui, model='quad', texture='../start/↑.png', scale=(0.25, 0.25), position=(0.55, -0.3), color=color.white, enabled=False)

    def lose_heart(self):
        if self.hearts:
            heart = self.hearts.pop()
            # تأثير بصري جميل عند فقد القلب
            heart.animate_scale(heart.scale * 1.4, duration=0.1)
            heart.animate_color(color.red, duration=0.2)
            invoke(destroy, heart, delay=0.4)

            if not self.hearts:
                print('😵 Game Over')
                application.quit()

    def enable_game_ui(self):
        self.score_text.enabled = True
        for heart in self.hearts:
            heart.enabled = True

    def disable_start_ui(self):
        self.start_button.enabled = False
        self.settings_button.enabled = False
        self.exit_button.enabled = False

    def enable_movement_buttons(self):
        self.right_btn.enabled = True
        self.left_btn.enabled = True
        self.jump_btn.enabled = True