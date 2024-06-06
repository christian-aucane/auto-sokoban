from pygame import mixer


class SoundManager:
    def __init__(self, music_volume=0.4, sound_effect_volume=1.0, num_channels=15):
        mixer.init()
        mixer.set_num_channels(num_channels)
        self._music_channels = {}
        self._music_channel = mixer.Channel(0)
        self._sound_effects_channels = {}
        self._music_volume = music_volume
        self._sound_effect_volume = sound_effect_volume

    def load_music(self, name, file_path):
        sound = mixer.Sound(file_path)
        sound.set_volume(self._music_volume)
        self._music_channels[name] = sound

    def play_music(self, name, loops=-1):
        print("PLAYING MUSIC", name)
        try:
            self._music_channel.play(self._music_channels[name], loops=loops)
        except KeyError:
            raise ValueError(f"Music '{name}' not found!")

    def stop_music(self):
        self._music_channel.stop()

    def load_sound_effect(self, name, file_path):
        sound = mixer.Sound(str(file_path))
        sound.set_volume(self._sound_effect_volume)
        channel = mixer.Channel(0)
        self._sound_effects_channels[name] = sound, channel

    def play_sound_effect(self, name):
        try:
            sound, channel = self._sound_effects_channels[name]
            channel.play(sound, loops=0)
        except KeyError:
            raise ValueError(f"Music '{name}' not found!")
        
    def stop_sound_effect(self, name):
        try:
            _, channel = self._sound_effects_channels[name]
            channel.stop()
        except KeyError:
            raise ValueError(f"Music '{name}' not found!")

    @property
    def music_volume(self):
        return self._music_volume

    @property
    def sound_effect_volume(self):
        return self._sound_effect_volume

    @music_volume.setter
    def music_volume(self, value):
        self._music_volume = value
        for sound in self._music_channels.values():
            sound.set_volume(value)

    @sound_effect_volume.setter
    def sound_effect_volume(self, value):
        self._sound_effect_volume = value
        for sound, _ in self._sound_effects_channels.values():
            sound.set_volume(value)

    @property
    def num_channels(self):
        return mixer.get_num_channels()
