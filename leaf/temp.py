import cv2, sys, time
import numpy

def a(dataDict):
    #print(data)
    # Create the haar cascade
    faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    #values = numpy.fromstring(data, sep='\t')
    #values = numpy.fromstring(data, dtype=numpy.int)
    data = dataDict['message']
    values = numpy.fromstring(data,dtype=numpy.uint8)
    values = values.reshape(dataDict['shape'][0], dataDict['shape'][1])
    print(values.shape)
    #print('VALUES', values)
    #start = time.time()
    faces = faceCascade.detectMultiScale(
    values,
    scaleFactor=1.1,
    minNeighbors=5,
    minSize=(30, 30),
    flags = cv2.IMREAD_GRAYSCALE
    )
    #print(time.time() - start)
    return str(str(dataDict['ticket']) + " Found {0} faces!".format(len(faces)))


#data = numpy.loadtxt('faceValue', dtype='uint8')
