import playsound

class SoundEffects:
    
    def play_change_mode(self):
        playsound.playsound("control/media/change_mode.mp3", True)

    def play_drive_mode(self):
        playsound.playsound("control/media/drive_mode.mp3", True)

    def play_robotic_arm_mode(self):
        playsound.playsound("control/media/robotic_arm_mode.mp3", True)

    def play_stationary_mode(self):
        playsound.playsound("control/media/stationary_mode.mp3", True)

    def play_emergency_stop_mode(self):
        playsound.playsound("control/media/emergency_stop.mp3", True)

