import pyrealsense2 as rs
import cv2 as cv
import numpy as np
import os 


pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.color,640,480,rs.format.bgr8,30)
pipeline.start(config)

face_cascade = cv.CascadeClassifier('/home/sdua078/chen_project/Rover/opportunity_code/control/opencv/data/haarcascades/haarcascade_frontalface_default.xml')
#alien_image = cv.imread('/home/sdua078/chen_project/Rover/opportunity_code/control/test1.png',flags=cv.IMREAD_UNCHANGED)
alien_image = cv.imread('/home/sdua078/chen_project/Rover/opportunity_code/control/alien.png')
#print('img',alien_image)

def detect_face(frame):
    gray = cv.cvtColor(frame,cv.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray,1.05,6) ##一个列表，里边每个元素
    return faces


def replace_face(frame, face, alien_image):
    #for (x,y,w,h) in faces:
    x,y,w,h = face[0], face[1],face[2],face[3]
    alien_resized = cv.resize(alien_image,(w,h))
    frame[y:y+h,x:x+w] = alien_resized #!!!!!!!!!!!!!!!!!!返回的xy有可能是box的左下角的xy的值
    return frame

def center(frame_shape, biggest_face):
    x,y,w,h = biggest_face[0],biggest_face[1],biggest_face[2],biggest_face[3]
    cx, cy = x+w//2, y+h//2 #center of biggest face
    fx, fy = frame_shape[1]//2, frame_shape[0]//2 #center of frame 

    move_x = cx-fx
    move_y = cy-fy
    if cx < 0:
        


try:
    while True:
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            continue
        
        frame = np.asanyarray(color_frame.get_data())
        faces = detect_face(frame)
        
        if len(faces) > 0:
            biggest_face = max(faces, key=lambda x: x[2]*x[3]) #x就代表列表的每一组数据，
            
            #x,y,w,h = biggest_face
            #cv.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)

            frame = replace_face(frame,biggest_face,alien_image)
            #print(frame.shape) #(480,640,3),h*w*c !!!是反过来的，提取frame center的时候别提取错了
        
        cv.imshow('ALien',frame) ##target been replaced, show whole frame ，实时显示
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    pipeline.stop()
    cv.destroyAllWindows()
        



# class FaceTracker:
#     def __init__(self, camera_index, Mast=None):

#         # Initialize the camera and face tracking parameters
#         self.capture = cv.VideoCapture(camera_index) # open video stream
#         self.frame_width = int(self.capture.get(cv.CAP_PROP_FRAME_WIDTH))
#         self.frame_height = int(self.capture.get(cv.CAP_PROP_FRAME_HEIGHT))
#         self.center_x = self.frame_width // 2
#         self.center_y = self.frame_height // 2
#         self.tolerance = 30  # How close to the center the object needs to be
#         self.max_speed = 100  # Maximum speed for movement
#         self.min_speed = 10   # Minimum speed for movement
#         #self.mast = mast # The Mast object to be controlled


#     def _get_face_position(self, frame):
#         """
#         Method for face detection.
#         This method returns the x, y coordinates of the face's center.
#         """
#         # currently uses haar cascade, which is quite sensitive
#         haar_cascade = cv.CascadeClassifier('haar_face.xml')          

#         gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY) # converts frame to grey scale

#         faces_rect = haar_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3) # higher minNeighbors, the less sensitive

#         # (x,y,w,h) = faces_rect # currently, only tracks the position of the first face of the array of detected faces
#         idx = 0
#         for i in range(len(faces_rect)):
#             x,y,w,h = faces_rect[i]
#             if i == 0: 
#                 largest = w*h
#             else: 
#                 if largest < w*h: 
#                     largest = w*h
#                     idx = i

#         x, y, w, h = faces_rect[0]
#         cv.rectangle(frame, (x,y), (x+w,y+h), (0,255,0), thickness=2)
#         cv.imshow('Frame', frame) 

#         return x, y


#     def _calculate_speed(self, distance):
#         """
#         This method returns the speed based on the distance from the center. Faster when further away.
#         """
#         # If the distance is within tolerance, return 0 (no movement)
#         if abs(distance) <= self.tolerance:
#             return 0

#         # Normalize the speed based on the distance, between min_speed and max_speed
#         speed = int((abs(distance) - self.tolerance) / (max(self.center_x, self.center_y) - self.tolerance) * (self.max_speed - self.min_speed) + self.min_speed)

#         return min(max(speed, self.min_speed), self.max_speed)


#     def track_face(self):
#         while True:
#             isTrue, frame = self.capture.read()

#             if not isTrue:
#                 print("Failed to read frame")    
#                 quit()

#             # Get the object's current position
#             face_x, face_y = self._get_face_position(frame)

#             # Calculate the distance from the center
#             x_distance = face_x - self.center_x
#             y_distance = face_y - self.center_y

#             # Calculate the speeds based on the distance
#             x_speed = self._calculate_speed(x_distance)
#             y_speed = self._calculate_speed(y_distance)

#             # Adjust the camera position based o
#         # If the distance is within tolerance, return 0 (no movement)
#         if abs(distancn the distance and speed
#             if x_speed > 0:
#                 if x_distance < 0:
#                     print("rotate counterclockwise")
#                     # self.mast.rotate_counterclockwise(x_speed)
#                 else:
#                     print("rotate clockwise")
#                     # self.mast.rotate_clockwise(x_speed)

#             if y_speed > 0:
#                 if y_distance < 0:
#                     print("tilt up")
#                     # self.mast.tilt_up(y_speed)
#                 else:
#                     print("tilt down")
#                     # self.mast.tilt_down(y_speed)

#             # cv.imshow('Frame', frame)

#             if cv.waitKey(1) & 0xFF == ord('q'): # This would need to be integrated with the xbox controller
#                 break

#         # Release the camera and close any open windows
#         self.capture.release()
#         cv.destroyAllWindows()