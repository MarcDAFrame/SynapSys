import cv2, sys, time
import numpy
import utils

def a(data):

    # Create the haar cascade
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    values = numpy.array(data)
	
    #start = time.time()
    faces = faceCascade.detectMultiScale(
        values,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags = cv2.IMREAD_GRAYSCALE
    )
    #print(time.time() - start)
    return str("Found {0} faces!".format(len(faces)))


#data = numpy.loadtxt('faceValue', dtype='uint8')
#print(a(data))
