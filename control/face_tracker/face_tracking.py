import pyrealsense2 as rs
import cv2 as cv
import numpy as np
import os 
import threading
import time
import random

class FaceTracker():
    
    IM_SIZE_H = 480
    IM_SIZE_W = 640
    MOVE_THRESHOLD = 1/8

    def __init__(self, replacement_mode='all'):
        self.replacement_mode = replacement_mode

        self.tilt_up = 0 # 1 if true, -1 if need to tilt down, 0 otherwise        
        self.move_right = 0 # 1 if true, -1 if need to move left, 0 otherwise        
        self.running = True

        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
        self.pipeline.start(self.config)
        
        self.face_cascade = cv.CascadeClassifier('control/face_tracker/haarcascade_frontalface_default.xml')

        # Load multiple alien images
        alien_image_paths = [
            os.path.join(os.getcwd(), 'control/face_tracker/alien_pictures/alien_1.png'),
            os.path.join(os.getcwd(), 'control/face_tracker/alien_pictures/alien_2.png'),
            os.path.join(os.getcwd(), 'control/face_tracker/alien_pictures/alien_3.png'),
            os.path.join(os.getcwd(), 'control/face_tracker/alien_pictures/alien_4.png')
        ]

        self.alien_image = cv.imread(random.choice(alien_image_paths), cv.IMREAD_UNCHANGED)

        # Create a thread for face detection and replacement
        self._face_detect_and_replace_thread = threading.Thread(
            target=self._face_detect_and_replace, args=()
        )
        self._face_detect_and_replace_thread.daemon = True
        self._face_detect_and_replace_thread.start()
        

    def detect_face(self,frame):
        gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray,1.05,6) 
        return faces


    # def replace_face(self,frame, faces, alien_image):
    #     biggest_face = max(faces, key=lambda x: x[2]*x[3]) 

    #     if self.replacement_mode == 'all':
    #         for (x, y, w, h) in faces:
    #             alien_resized = cv.resize(alien_image,(w,h))
    #             frame[y:y+h,x:x+w] = alien_resized 
    #     else:
    #         x,y,w,h = biggest_face[0], biggest_face[1], biggest_face[2], biggest_face[3]
    #         alien_resized = cv.resize(alien_image,(w,h))
    #         frame[y:y+h,x:x+w] = alien_resized 

    #     return frame, biggest_face


    def replace_face(self, frame, faces, alien_image, scale_factor=2):
        # Check if the alien image has an alpha channel
        if alien_image.shape[2] != 4:
            raise ValueError("Alien image does not have an alpha channel. Make sure it's a 4-channel PNG image.")

        biggest_face = max(faces, key=lambda x: x[2] * x[3])

        def blend_alien(roi, alien_resized):
            # Extract the RGB and alpha channels from alien_resized
            alien_rgb = alien_resized[:, :, :3]  # The color part (RGB)
            alien_alpha = alien_resized[:, :, 3] / 255.0  # Normalize the alpha channel to 0-1

            # Perform alpha blending
            for c in range(3):  # Iterate over the color channels (B, G, R)
                roi[:, :, c] = (alien_alpha * alien_rgb[:, :, c] + (1 - alien_alpha) * roi[:, :, c])
            return roi

        if self.replacement_mode == 'all':
            for (x, y, w, h) in faces:
                # Calculate new dimensions considering the scale factor
                new_w = int(w * scale_factor)
                new_h = int(h * scale_factor)

                # Resize the alien image to the scaled face dimensions
                alien_resized = cv.resize(alien_image, (new_w, new_h))

                # Extract the region of interest (ROI) in the frame where the face is
                roi_x_start = x - int((new_w - w) / 2)
                roi_y_start = y - int((new_h - h) / 2)

                # Ensure ROI coordinates are within frame boundaries
                roi_x_start = max(0, roi_x_start)
                roi_y_start = max(0, roi_y_start)
                roi_x_end = min(frame.shape[1], roi_x_start + new_w)
                roi_y_end = min(frame.shape[0], roi_y_start + new_h)

                # Ensure ROI dimensions match the resized alien image
                roi = frame[roi_y_start:roi_y_end, roi_x_start:roi_x_end]

                # Resize alien_resized to match the ROI dimensions if necessary
                if alien_resized.shape[0] != roi.shape[0] or alien_resized.shape[1] != roi.shape[1]:
                    alien_resized = cv.resize(alien_resized, (roi.shape[1], roi.shape[0]))

                # Blend the alien image with the frame
                frame[roi_y_start:roi_y_end, roi_x_start:roi_x_end] = blend_alien(roi, alien_resized)

        elif self.replacement_mode == 'biggest':
            x, y, w, h = biggest_face

            # Calculate new dimensions considering the scale factor
            new_w = int(w * scale_factor)
            new_h = int(h * scale_factor)

            # Resize the alien image to the scaled face dimensions
            alien_resized = cv.resize(alien_image, (new_w, new_h))

            # Extract the region of interest (ROI) in the frame where the biggest face is
            roi_x_start = x - int((new_w - w) / 2)
            roi_y_start = y - int((new_h - h) / 2)

            # Ensure ROI coordinates are within frame boundaries
            roi_x_start = max(0, roi_x_start)
            roi_y_start = max(0, roi_y_start)
            roi_x_end = min(frame.shape[1], roi_x_start + new_w)
            roi_y_end = min(frame.shape[0], roi_y_start + new_h)

            # Ensure ROI dimensions match the resized alien image
            roi = frame[roi_y_start:roi_y_end, roi_x_start:roi_x_end]

            # Adjust dimensions if necessary to fit within the ROI
            if alien_resized.shape[0] > roi.shape[0] or alien_resized.shape[1] > roi.shape[1]:
                alien_resized = cv.resize(alien_resized, (roi.shape[1], roi.shape[0]))

            # Blend the alien image with the frame
            frame[roi_y_start:roi_y_end, roi_x_start:roi_x_end] = blend_alien(roi, alien_resized)

        return frame, biggest_face


    def move_calculate(self,frame_shape, biggest):

        x,y,w,h = biggest[0],biggest[1],biggest[2],biggest[3]
        cx, cy = x+w//2, y+h//2 #center of biggest face
        fx, fy = frame_shape[1]//2, frame_shape[0]//2 #center of frame (480,640,3)

        move_x = fx - cx # +ve if fx greater than cx (i.e., to the left)
        move_y = fy - cy # +ve if fy greater than cy (i.e., in the upper region)
        # check the location of the biggest face in the horizontal direction
        if move_x < -(self.IM_SIZE_W * self.MOVE_THRESHOLD):
            self.move_right = 1
        elif move_x > self.IM_SIZE_W * self.MOVE_THRESHOLD:
            self.move_right = -1
        else: 
            self.move_right = 0
        
        # check the location of the biggest face in the vertical direction
        if move_y > self.IM_SIZE_H * self.MOVE_THRESHOLD:
            self.tilt_up = 1
        elif move_y < -(self.IM_SIZE_H * self.MOVE_THRESHOLD):
            self.tilt_up = -1
        else: 
            self.tilt_up = 0

        return move_x, move_y


    def realtime_track(self):

        frames = self.pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()

        if not color_frame:
            return None
        
        frame = np.asanyarray(color_frame.get_data())
        faces = self.detect_face(frame)

        if len(faces) > 0:
            frame, biggest_face = self.replace_face(frame, faces, self.alien_image)
            _, _ = self.move_calculate(frame.shape, biggest_face)
            
        return frame


    def release(self):
        self.pipeline.stop()
        cv.destroyAllWindows()
        self.running = False


    def get_move_vertical(self): # +ve if need to move up, -ve down, 0 otherwise
        return self.tilt_up


    def get_move_horizontal(self): # +ve if need to move right, -ve left, 0 otherwise
        return self.move_right


    def is_facetracker(self):
        return self.running


    def _face_detect_and_replace(self):
        try:
            cv.namedWindow("Alien", cv.WINDOW_NORMAL)
            while True:
                frame = self.realtime_track()

                if frame is not None:
                    frame = cv.resize(frame, dsize=(2880,1800), interpolation=cv.INTER_CUBIC)
                    cv.imshow('Alien',frame) 

                if cv.waitKey(1) & 0xFF == ord('q'):
                    break

        finally:
            self.release()
                

if __name__ == '__main__':
    facetracker = FaceTracker(replacement_mode='all')
    
    # example of how to get the direction for the mast
    while facetracker.is_facetracker(): 
        print(f'move right: {facetracker.get_move_horizontal()}')
        print(f'move up: {facetracker.get_move_vertical()}')
        time.sleep(1)
