import argparse
import cv2

# get img from dir
parser = argparse.ArgumentParser()
parser.add_argument('--path', default='../../OpenCV-3-Computer-Vision-with-Python-Cookbook/data/Lena.png', help='Image path.')
parser.add_argument('--out_png', default='./Lena_compressed.png',
                    help='Output image path for lossless result.')
parser.add_argument('--out_jpg', default='./Lena_compressed.jpg',
                    help='Output image path for lossy result.')
params = parser.parse_args()
img = cv2.imread(params.path)
print('original image shape:', img.shape)

#이미지를 저장
cv2.imwrite(params.path, img,
            [cv2.IMWRITE_PNG_COMPRESSION, 0])

#이미지를 다시 불러들여 원본과 비교
saved_img = cv2.imread(params.out_png)
assert saved_img.all() == img.all()

#이미지를 낮은 화질로 저장
cv2.imwrite(params.out_jpg, img,
            [cv2.IMWRITE_JPEG_QUALITY,80])

