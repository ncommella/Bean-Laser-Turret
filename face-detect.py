import cv2
import pyfirmata
import numpy as np
from cvzone.FaceDetectionModule import FaceDetector
from time import sleep

#TODO: remove cvzone and use cv2
#   smooth aiming - use average of 3 readings?
cap = cv2.VideoCapture(0)
detector = FaceDetector()

board = pyfirmata.Arduino('/dev/ttyACM0')
it = pyfirmata.util.Iterator(board)
it.start()

panServo = board.get_pin('d:9:s')
tiltServo = board.get_pin('d:6:s')

def convert_to_servo_angle (x, y):
    converted_X = np.interp(x, [0, 640], [0, 180])
    converted_Y = np.interp(y, [0, 480], [0, 180])

    return converted_X, converted_Y

def move_servos(pan, tilt):
    panServo.write(180 - pan)
    tiltServo.write(180 - tilt)

while True:
    success, img = cap.read()
    img, bboxs = detector.findFaces(img)

    if bboxs:
        center_X = bboxs[0]['center'][0]
        center_Y= bboxs[0]['center'][1]
        print(bboxs[0]['center'])
        print(convert_to_servo_angle(center_X, center_Y))
        pan, tilt = convert_to_servo_angle(center_X, center_Y)
        move_servos(pan, tilt)
    else:
        move_servos(90, 90)


    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
