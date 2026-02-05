from ursina import *

class SettingsPanel:
    def __init__(self):
        self.master_volume_slider = Slider(min=0, max=1, default=1, step=0.01, dynamic=True)
        self.sound_volume_slider = Slider(min=0, max=1, default=1, step=0.01, dynamic=True)
        self.music_volume_slider = Slider(min=0, max=1, default=1, step=0.01, dynamic=True)

        self.panel = WindowPanel(
            title='Settings',
            content=(
                Text('Master Volume:'),
                self.master_volume_slider,
                Text('Sounds/tap-b.ogg'),
                self.sound_volume_slider,
                Text('Music Volume:'),
                self.music_volume_slider,
                Button(text='Close', color=color.red, on_click=self.close)
            ),
            position=(0, 0),
            enabled=False
        )

    def show(self):
        self.panel.enabled = True

    def close(self):
        self.panel.enabled = False
