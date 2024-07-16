import cv2 as cv

#define camera
def Camera(ID=0, Preference=cv.CAP_DSHOW):
    capture = cv.VideoCapture(ID,apiPreference=Preference)                          # Getting camera frame by frame
    fokus = 0                                                                       # set fokus to 0 (why 0? Just because it worked for us)
    capture.set(28,fokus)                                                           # Call camera manually to set fokus
    IsTrue, camera = capture.read()                                                 # Read capture and get RGB Picture
    return (capture, camera)