import cv2

cam = cv2.VideoCapture(0)

while cam.isOpened():
    _, image = cam.read()
    image = cv2.GaussianBlur(image, (11, 11), 3)
    len1 = len(image); len2 = len(image[len1-1])
    image = cv2.putText(image, str(image[int(len1/2)][int(len2/2)]), (10,60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (100,100,255),2)
    image[int(len1/2), int(len2/2)] = 0
    image[int(len1/2-2):int(len1/2+2):1, int(len2/2-2):int(len2/2+2):1] = 0
    cv2.imshow("image", image)
    key = cv2.waitKey(1)
    if key == "q":
        pass
cv2.destroyAllWindows()

# yellow: 130,170,170 - 16,130,135 (32, 132, 134)
# red: 90.64.185 - 18.22.80 (5, 8, 50 - 28.20.130)
# blue: 165.60.40 - 80.16.16 (70, 8, 0 - 120, 45, 30)