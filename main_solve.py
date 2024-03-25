from find import extract_digit, find_puzzle
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import GUI
import numpy as np
import argparse
import imutils
import cv2
import kivy

ap = argparse.ArgumentParser()
ap.add_argument("-m", "--model", default="digit_classifier.h5", help="Path to digit classifier model")
ap.add_argument("-i", "--image", default="sudoku.jpg", help="Path to the input image")
ap.add_argument("-d", "--debug", type=int, default=-1, help="Activate debug images for the extraction pipeline")
args = vars(ap.parse_args())

print("[INFO] loading digit classifier...")
model = load_model(args["model"])
print("[INFO] Processing Image...")
image = cv2.imread(args["image"])
image = imutils.resize(image, width=600)
(puzzle, warped) = find_puzzle(image, debug=args["debug"] > 0)
board = []
for i in range(9):
    line = []
    for j in range(9):
        line.append(0)
    board.append(line)

stepX = warped.shape[1] // 9
stepY = warped.shape[0] // 9

cellLocs = []
for y in range(0,9):
    row = []
    for x in range(0, 9):
        startX = x*stepX
        startY = y*stepY
        endX = (x+1)*stepX
        endY = (y+1)*stepY
        cell = warped[startY:endY, startX:endX]
        digit = extract_digit(cell, debug=args["debug"] > 0)
        row.append(((startX, startY, endX, endY), digit))
        if digit is not None:
            roi = cv2.resize(digit, (28,28))
            roi = roi.astype("float") / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)
            pred = model.predict(roi).argmax(axis=1)[0]
            board[y][x] = pred
    cellLocs.append(row)
GUI.main(board)
for (cellRow, boardRow) in zip(cellLocs, board):
    for (box, digit) in zip(cellRow, boardRow):
        if box[1] is None:
            startX, startY, endX, endY = box[0]
            textX = startX + int((endX - startX) * 0.33)
            textY = endY + int((endY - startY) * -0.2)
            cv2.putText(puzzle, str(digit), (textX, textY), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0,255, 255), 2)
cv2.imshow("Sudoku Result", puzzle)
cv2.waitKey(0)