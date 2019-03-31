import argparse
import cv2

# get img path from dir
parser = argparse.ArgumentParser()
parser.add_argument('--path', default='../../OpenCV-3-Computer-Vision-with-Python-Cookbook/data/Lena.png', help='Image path.')
params = parser.parse_args()

#이미지를 불러오고 크기를 얻는다.
orig = cv2.imread(params.path)
orig_size = orig.shape[0:2]
print('original image shape:', orig.shape)

#이미지를 표시하기 위한 윈도우 호출
cv2.imshow("Original image", orig)
cv2.waitKey(2000)
