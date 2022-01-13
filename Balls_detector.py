import cv2

#Предподготовленные данные
cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

yellow = {"lower": (30, 100, 120), "upper": (75, 200, 200)}
red = {"lower": (10, 10, 90), "upper": (50, 50, 140)}
blue = {"lower": (70, 10, 10), "upper": (180, 50, 40)}


#Рабочий код
def detect_ball(image, lower, upper):
    pass

while cam.isOpened():
    _, image = cam.read()
    blurred = cv2.GaussianBlur(image,(7,7), 3)
    #hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(blurred, yellow["lower"], yellow["upper"])
    mask = cv2.erode(mask, None, iterations = 2)
    mask = cv2.dilate(mask, None, iterations = 2)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    
    if len(cnts) > 0:
        c = max(cnts, key = cv2.contourArea)
        (curr_x,curr_y), radius = cv2.minEnclosingCircle(c)
        if radius > 10:
            cv2.circle(image,(int(curr_x), int(curr_y)), 5, (0,255,255),2)
            cv2.circle(image,(int(curr_x), int(curr_y)), int(radius), (0,255,255), 2)
    cv2.imshow("Camera",image)
    cv2.imshow("mask",mask)
    key = cv2.waitKey(1)
    if key == ord("q"):
        break

cam.release()
cv2.destroyAllWindows()