import playsound
import threading
import random
import time
"""
Robot Sounds from https://pixabay.com/sound-effects/search/robot%20sounds/
"""
class SoundEffects:

    def __init__(self):
        self.background_sounds = threading.Thread(target=self.run_background_sounds)
        self.background_sounds.start()
    
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

    def play_happy_birthay(self):
        playsound.playsound("control/media/happy_birthday.mp3", True)
    
    def run_background_sounds(self):

        while True:
            
            # Sing happy birthday if it is the rover's birthday, every hour on that day
            if time.localtime().tm_mon == 7 and time.localtime().tm_mday == 7 and time.localtime().tm_min == 0:
                self.play_happy_birthay()

            # Random chance to play a random sound effect
            if random.randint(0, 3) == 0:

                # Randomly select a sound effect from 13 different sound effects
                sound_effect = random.randint(0, 12)

                if sound_effect == 0:
                    playsound.playsound("control/media/robot_sounds/robot_sound_1.mp3", True)
                elif sound_effect == 1:
                    playsound.playsound("control/media/robot_sounds/robot_sound_2.mp3", True)
                elif sound_effect == 2:
                    playsound.playsound("control/media/robot_sounds/robot_sound_3.mp3", True)
                elif sound_effect == 3:
                    playsound.playsound("control/media/robot_sounds/robot_sound_4.mp3", True)
                elif sound_effect == 4:
                    playsound.playsound("control/media/robot_sounds/robot_sound_5.mp3", True)
                elif sound_effect == 5:
                    playsound.playsound("control/media/robot_sounds/robot_sound_6.mp3", True)
                elif sound_effect == 6:
                    playsound.playsound("control/media/robot_sounds/robot_sound_7.mp3", True)
                elif sound_effect == 7:
                    playsound.playsound("control/media/robot_sounds/robot_sound_8.mp3", True)
                elif sound_effect == 8:
                    playsound.playsound("control/media/robot_sounds/robot_sound_9.mp3", True)
                elif sound_effect == 9:
                    playsound.playsound("control/media/robot_sounds/robot_sound_10.mp3", True)
                elif sound_effect == 10:
                    playsound.playsound("control/media/robot_sounds/robot_sound_11.mp3", True)
                elif sound_effect == 11:
                    playsound.playsound("control/media/robot_sounds/robot_sound_12.mp3", True)
                elif sound_effect == 12:
                    playsound.playsound("control/media/robot_sounds/robot_sound_13.mp3", True)
                
                # Sleep for a random amount of time
            time.sleep(random.randint(5, 15))
            
        
# Main test function
if __name__ == "__main__":
    sound_effects = SoundEffects()