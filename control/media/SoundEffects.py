import vlc


class SoundEffects:
    def __init__(self):
        self.change_mode = vlc.MediaPlayer("control/media/SoundEffects.py")
        self.drive_mode = vlc.MediaPlayer("file:///path/to/track.mp3")
        self.robotic_arm_mode = vlc.MediaPlayer("file:///path/to/track.mp3")
        self.stationary_mode = vlc.MediaPlayer("file:///path/to/track.mp3")
        self.emergency_stop_mode = vlc.MediaPlayer("file:///path/to/track.mp3")
    
    def play_change_mode(self):
        self.change_mode.play()

    def play_drive_mode(self):
        pass

    def play_robotic_arm_mode(self):
        pass

    def play_stationary_mode(self):
        pass

    def play_emergency_stop_mode(self):
        pass

