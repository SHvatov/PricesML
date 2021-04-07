import cv2

def check_area(area, image_area):
    return area / image_area < 0.95

def crop_image(image_path):
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
        cv2.imwrite(image_path, roi)