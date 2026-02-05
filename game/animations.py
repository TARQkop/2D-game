import os
from ursina import load_texture

# الحصول على مسار المجلد الحالي للملف
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

# قائمة الملفات للأنيميشن بدلاً من تحميلها مباشرة
folders = {
    'idle': 'Idle_KG_1',
    'idle_left': 'Idle_KG_2',
    'run': 'Walking_KG_1',
    'run_left': 'Walking_KG_2',
    'jump': 'Jump_KG_1',
    'jump_left': 'Jump_KG_2',
}

animation_files = {}
for name, folder in folders.items():
    animation_files[name] = sorted([f for f in os.listdir(os.path.join(parent_dir, folder)) if f.endswith('.png')])

# تحميل الأنيميشن عند الحاجة
animations = {}

def load_animation(name):
    if name not in animations:
        folder = folders[name]
        animations[name] = [load_texture(f'../{folder}/{f}')
                           for f in animation_files[name]]
    return animations[name]

# التحقق من وجود الإطارات
for key, frames in animation_files.items():
    if not frames:
        print(f'no frames found for animation: {key}')
        exit()