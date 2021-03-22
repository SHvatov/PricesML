import cv2
import random


def check_area(area, image_area):
    return area / image_area < 0.95


def detect_objects(image_path):
    res = list()
    r = random.randint(0, 1000000)
    for i in range(0, 11, 1):
        image_path = detect_object(image_path, i + r)
        if image_path == "":
            break
        res.append(image_path)

    return res


def detect_object(image_path, i):
    img = cv2.imread(image_path)
    height, width, channels = img.shape
    image_area = height * width
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    retval, thresh_gray = cv2.threshold(gray, thresh=100, maxval=255,
                                        type=cv2.THRESH_BINARY_INV)

    contours, hierarchy = cv2.findContours(thresh_gray, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    mx = (0, 0, 0, 0)
    mx_area = 0
    for cont in contours:
        x, y, w, h = cv2.boundingRect(cont)
        area = w * h
        if area > mx_area and check_area(area, image_area):
            mx = x, y, w, h
            mx_area = area
    x, y, w, h = mx

    roi = img[y:y + h, x:x + w]

    if roi.any():
        name = 'object' + str(i) + '.jpg'
        cv2.imwrite(name, roi)
    else:
        name = ""

    return name


#print(detect_objects("E:\python_proj\PricesML\objects-detection\detection\img\i16.jpg"))
