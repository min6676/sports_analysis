import argparse
import cv2, numpy as np

# get img path from dir
parser = argparse.ArgumentParser()
parser.add_argument('--path', default='../../OpenCV-3-Computer-Vision-with-Python-Cookbook/data/Lena.png', help='Image path.')
params = parser.parse_args()

cv2.namedWindow('window')
fill_val = np.array([255, 255, 255], np.uint8)

#색상 구성요소 인덱스와 설정될 새 값을 받음
def trackbar_callback(idx, value):
    fill_val[idx] = value

#세개의 탐색바를 윈도우에 추가.
cv2.createTrackbar('R', 'window', 255, 255, lambda v:
                   trackbar_callback(2,v))
cv2.createTrackbar('G', 'window', 255, 255, lambda v:
                   trackbar_callback(1,v))
cv2.createTrackbar('B', 'window', 255, 255, lambda v:
                   trackbar_callback(0,v))

#루프에서 세개의 트랙바와 키보드 입력을 처리하는 창에 이미지 표시.
while True:
    image = np.full((500, 500, 3), fill_val)
    cv2.imshow('window', image)
    key = cv2.waitKey(3)
    if key == 27:
        break
cv2.destroyAllWindows()