import cv2

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)

Balls = { "yellow": {"lower": (30, 100, 120), "upper": (75, 200, 200), "posx": -1, "posy": -1, "radius": -1, "name": "Yellow "},
"red": {"lower": (10, 10, 100), "upper": (55, 55, 160), "posx": -1, "posy": -1, "radius": -1, "name": "Red "},
"blue": {"lower": (70, 10, 10), "upper": (190, 55, 45), "posx": -1, "posy": -1, "radius": -1, "name": "Blue "}
}

def keyx(e):
    return Balls[e]["posx"]
def keyy(e):
    return Balls[e]["posy"]

#Функция определяет шарик по цвету.
def detect_ball(blurred, lower, upper):
    mask = cv2.inRange(blurred, lower, upper)
    mask = cv2.erode(mask, None, iterations = 2)
    mask = cv2.dilate(mask, None, iterations = 2)
    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    if len(cnts) > 0:
        c = max(cnts, key = cv2.contourArea)
        (curr_x,curr_y), radius = cv2.minEnclosingCircle(c)
        return curr_x, curr_y, radius
    else:
        return -1, -1, -1

def mark_ball(image, x, y, radius, color):
    if radius > 10:
        cv2.circle(image,(int(x), int(y)), 5, color,2)
        cv2.circle(image,(int(x), int(y)), int(radius), color, 2)
    return image

while cam.isOpened():
    _, image = cam.read()
    blurred = cv2.GaussianBlur(image,(7,7), 3)
    Balls["red"]["posx"], Balls["red"]["posy"], Balls["red"]["radius"] = detect_ball(blurred, Balls["red"]["lower"], Balls["red"]["upper"])
    Balls["blue"]["posx"], Balls["blue"]["posy"], Balls["blue"]["radius"] = detect_ball(blurred, Balls["blue"]["lower"], Balls["blue"]["upper"])
    Balls["yellow"]["posx"], Balls["yellow"]["posy"], Balls["yellow"]["radius"] = detect_ball(blurred, Balls["yellow"]["lower"], Balls["yellow"]["upper"])
    image = mark_ball(image, Balls["red"]["posx"], Balls["red"]["posy"], Balls["red"]["radius"], Balls["red"]["upper"])
    image = mark_ball(image, Balls["blue"]["posx"], Balls["blue"]["posy"], Balls["blue"]["radius"], Balls["blue"]["upper"])
    image = mark_ball(image, Balls["yellow"]["posx"], Balls["yellow"]["posy"], Balls["yellow"]["radius"], Balls["yellow"]["upper"])
    
    if Balls["red"]["posx"] != -1 or Balls["blue"]["posx"] != -1 or Balls["yellow"]["posx"] != -1:
        order = "From left to right: "
        for key in sorted(Balls.keys(), key=keyx):
            if Balls[key]["posx"] != -1:
                order += Balls[key]["name"]
        order2 = "From up to down: "
        for key in sorted(Balls.keys(), key = keyy):
            if Balls[key]["posy"] != -1:
                order2 += Balls[key]["name"]
        cv2.putText(image, order, (10,30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0),2)
        cv2.putText(image, order2, (10,60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0),2)
    cv2.imshow("Camera",image)
    key = cv2.waitKey(1)
    if key == ord("q"):
        break

cam.release()
cv2.destroyAllWindows()