from ursina import *
from player import Player
from items import Apple, Bomb
from ui import UI
from settings import SettingsPanel
import random
import os

# الحصول على مسار المجلد الأساسي
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# إعدادات اللعبة
app = Ursina()
score = [0]  # استخدام قائمة لتعديل القيمة داخل الدوال
settings_panel = SettingsPanel()

# إعدادات النافذة
window.size = (1600, 900)
window.title = 'the game'
window.fullscreen = False
window.borderless = False
window.vsync = True
window.exit_button.visible = False
window.fps_counter.enabled = False
window.orthographic = True
window.show_orthographic_grid = False
camera.orthographic = True
camera.fov = 16

# شاشة البدء
show_start_screen = True
start_bg = Entity(model='quad', texture='../You may also like/Background.png', scale=(32, 16), z=-10)
main_bg = Entity(model='quad', texture='../You may also like/Pixel Art Forest.png', scale=(32, 16), z=1, enabled=False)

# الأرض
ground = Entity(model='quad', color=color.green, scale=(20, 1), position=(0, -10), collider='box')

# إنشاء الكائنات
ui = UI()
player = Player(ground=ground)

# ضبط موضع اللاعب على الأرض
player.y = ground.y + ground.scale_y / 2 + player.scale_y / 2

# ربط أزرار الحركة
ui.right_btn.on_click = player.hold_right
ui.right_btn.on_release = player.release_right
ui.left_btn.on_click = player.hold_left
ui.left_btn.on_release = player.release_left
ui.jump_btn.on_click = player.jump

# دالة خسارة القلب
def lose_heart():
    ui.lose_heart()

# بدء اللعبة
def start_game():
    global show_start_screen

    show_start_screen = False
    start_bg.enabled = False
    main_bg.enabled = True

    ui.disable_start_ui()
    ui.enable_movement_buttons()
    ui.enable_game_ui()

    score[0] = 0
    ui.score_text.text = f"Points: {score[0]}"
    ui.score_text.position = (0.70, 0.45)

    invoke(spawn_items, delay=2)

def spawn_items():
    drop_type = random.choice(['apple', 'bomb'])
    x_pos = random.uniform(-6, 6)
    if drop_type == 'apple':
        apple = Apple(position=(x_pos, 5), score_ref=score, score_text_ref=ui.score_text)
        apple.set_player(player)
    else:
        Bomb(position=(x_pos, 5), player=player, lose_heart_callback=lose_heart)
    invoke(spawn_items, delay=2.5)

# ربط أزرار البداية
ui.start_button.on_click = start_game
ui.exit_button.on_click = application.quit
ui.settings_button.on_click = settings_panel.show

# تحديث اللعبة
def update():
    if show_start_screen:
        return

    # تحديث جميع الكائنات
    for e in scene.entities:
        if hasattr(e, 'update'):
            e.update()

    # دعم الأزرار اللمسية
    player.right_held = ui.right_btn.enabled and ui.right_btn.hovered and held_keys['left mouse']
    player.left_held = ui.left_btn.enabled and ui.left_btn.hovered and held_keys['left mouse']

    # فحص التصادم مع الأرض
    player.check_ground_collision()

# قفز بزر المسافة
def input(key):
    if key == 'space' and not player.is_jumping and not show_start_screen:
        player.jump()

if __name__ == '__main__':
    app.run()