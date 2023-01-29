import numpy as np
import pytesseract as pt
import cv2
from PIL import Image


def preprocess(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 
    blur = cv2.GaussianBlur(gray, (3, 3), 6) 
    thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)
    return thresh


def main_outline(contour):
    biggest = np.array([])
    max_area = 0
    for i in contour:
        area = cv2.contourArea(i)
        if area > 50:
            perimeter = cv2.arcLength(i, True)
            approx = cv2.approxPolyDP(i , 0.02 * perimeter, True)
        if area > max_area and len(approx) == 4:
            biggest = approx
            max_area = area
        return biggest, max_area
    

def reframe(points):
    points = points.reshape((4, 2))
    new_points = np.zeros((4,1,2), dtype=np.int32)
    add = points.sum(1)
    new_points[0] = points[np.argmin(add)]
    new_points[3] = points[np.argmax(add)]
    diff = np.diff(points, axis=1)
    new_points[1] = points[np.argmin(diff)]
    new_points[2] = points[np.argmax(diff)]
    return new_points


def split_cells(img):
    rows = np.vsplit(img, 9)
    boxes = []
    for r in rows:
        cols = np.hsplit(r, 9)
        for box in cols:
            boxes.append(box)
    return boxes


def crop_cells(cells):
    cropped = []
    for image in cells:
        cell = np.array(image)
        cell = cell[4:46, 6:46]
        cell = Image.fromarray(cell)
        cropped.append(cell)
    return cropped


def find_digit(s):
    for c in s:
        if c.isdigit():
            return int(c)
    return 0


def ocr(img_path):
    grid = np.array([[0 for _ in range(9)] for _ in range(9)])
    pt.pytesseract.tesseract_cmd = r'D:\Tesseract\tesseract'
    img_path = cv2.imread(img_path)
    img_path = cv2.resize(img_path, (450,450))
    threshold = preprocess(img_path)
    contour1 = contour2 = img_path.copy()
    contour, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(contour1, contour, -1, (0, 255, 0), 3)
    biggest, _ = main_outline(contour)
    if biggest.size != 0:
        biggest = reframe(biggest)
    if not biggest.size:
        return np.array([])
    cv2.drawContours(contour2, biggest, -1, (0, 255, 0), 10)
    pts1 = np.float32(biggest)
    pts2 = np.float32([[0, 0], [450, 0], [0, 450], [450, 450]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imagewrap = cv2.warpPerspective(img_path, matrix, (450, 450))
    imagewrap = cv2.cvtColor(imagewrap, cv2.COLOR_BGR2GRAY)
    split = split_cells(imagewrap)
    cells = crop_cells(split)
    for i, cell in enumerate(cells):
        x, y = i // 9, i % 9
        text = pt.image_to_string(cell, config=r'--oem 3 --psm 13')
        if text:
            grid[x, y] = find_digit(text)
    return grid

if __name__ == '__main__':
    print(ocr('bb.png'))