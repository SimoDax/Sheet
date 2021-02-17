import cv2 as cv
import numpy as np

''' Vertical sheet? '''

# width = 720
# height = int(width*1.414) 

''' Horizontal sheet? '''

height = 1000
width = int(height*1.414)

''' Convert to grayscale? '''

grayscale = False

''' More than one camera? '''

camera_index = 0



points = np.empty((0,2), dtype=np.float32)
dest = np.float32([[0,0], [width, 0], [0, height], [width, height]])

tform = None

def click(event, x, y, flags, param):
    global tform, points

    if event == cv.EVENT_LBUTTONUP:
	    points = np.append(points, [[x, y]], axis=0)

    if points.shape[0] == 4:
        tform = cv.getPerspectiveTransform(points.astype(np.float32), dest.astype(np.float32))

def as_tuple(p):
    return (p[0], p[1])


cap = cv.VideoCapture()
cap.open(camera_index)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 1920)        # set to 1280 if you don't have a Full HD webcam

cv.namedWindow("source")
cv.setMouseCallback("source", click)

while True:
    _, img = cap.read()

    if tform is None:
        if len(points) > 1:
            cv.line(img, as_tuple(points[0].astype(np.int)), as_tuple(points[1].astype(np.int)), (0,0,255),2)
        if len(points) > 2:
            cv.line(img, as_tuple(points[0].astype(np.int)), as_tuple(points[2].astype(np.int)), (0,0,255),2)

        cv.imshow("source", img)
    else:
        sheet = cv.warpPerspective(img, tform, (width, height))

        if grayscale:
            sheet = cv.cvtColor(sheet, cv.COLOR_BGR2GRAY)
            sheet = cv.normalize(sheet, None, alpha = 0, beta = 255, norm_type = cv.NORM_MINMAX, dtype = cv.CV_32F)
            sheet = sheet.astype(np.uint8)

        cv.imshow("sheet", sheet)

    cv.waitKey(15)
