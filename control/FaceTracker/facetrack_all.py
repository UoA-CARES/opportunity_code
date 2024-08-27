import pyrealsense2 as rs
import cv2 as cv
import numpy as np
import os 

class FaceTracker():
    def __init__(self):

        self.pipeline = rs.pipeline()
        self.config = rs.config()
        self.config.enable_stream(rs.stream.color,640,480,rs.format.bgr8,30)
        self.pipeline.start(self.config)
        
        # self.face_cascade = cv.CascadeClassifier(os.path.join(os.getcwd(), 'opencv\\data\\haarcascades\\haarcascade_frontalface_default.xml'))
        self.face_cascade = cv.CascadeClassifier('haarcascade_frontalface_default.xml')
        alien_image_path = os.path.join(os.getcwd(),'alien_pictures/dab1.png')
        #alien_image_path = os.path.join(os.getcwd(),'alien_pictures/greensmileface.png')
        #alien_image_path = os.path.join(os.getcwd(),'alien_pictures/purplealien.png')
        #alien_image_path = os.path.join(os.getcwd(),'alien_pictures/spongebob.png')

        self.alien_image = cv.imread(alien_image_path)


    def detect_face(self,frame):
        gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
        faces = self.face_cascade.detectMultiScale(gray,1.05,6) 
        return faces


    def replace_face(self,frame, face, alien_image):
        for (x, y, w, h) in face:
            alien_resized = cv.resize(alien_image,(w,h))
            frame[y:y+h,x:x+w] = alien_resized 
        return frame


    def move_calculate(self,frame_shape, biggest):
        x,y,w,h = biggest[0],biggest[1],biggest[2],biggest[3]
        cx, cy = x+w//2, y+h//2 #center of biggest face
        fx, fy = frame_shape[1]//2, frame_shape[0]//2 #center of frame (480,640,3)

        move_x = cx-fx
        move_y = cy-fy
        return move_x, move_y


    def realtime_track(self):

        frames = self.pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            return None
        
        frame = np.asanyarray(color_frame.get_data())
        faces = self.detect_face(frame)
        biggest_face = None
        if len(faces) > 0:
            biggest_face = max(faces, key=lambda x: x[2]*x[3]) 
            frame = self.replace_face(frame,faces,self.alien_image)
            #moveX, moveY = self.move_calculate(frame.shape, biggest_face)
            
        return frame, biggest_face


    def release(self):
        self.pipeline.stop()
        cv.destroyAllWindows()
            

if __name__ == '__main__':
    facetracker = FaceTracker()
    try:
        while True:
            frame, biggestFace = facetracker.realtime_track()
            if frame is not None and biggestFace is not None:
                x_move, y_move = facetracker.move_calculate(frame.shape,biggestFace)
                cv.imshow('ALien',frame) 
            elif frame is not None:
                cv.imshow('ALien',frame) 
            if cv.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        facetracker.release()
