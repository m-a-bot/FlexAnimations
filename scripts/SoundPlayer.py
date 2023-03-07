import arcade
import scipy.io.wavfile

class SoundPlayer:
    
    def __init__(self, file_name):
        
        self.sound = arcade.load_sound(file_name)
        self.wave_data = scipy.io.wavfile.read(file_name)

        self.volume = 1
        self.looping = False
        self.speed = 1

        self.player = None

    
    def play(self):
        self.player = arcade.play_sound(self.sound, self.volume, looping = self.looping, speed = self.speed)

    
    def stop(self):
        if self.player != None:
            arcade.stop_sound(self.player)