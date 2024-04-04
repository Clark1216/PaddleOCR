from paddleocr import PaddleOCR, draw_ocr
import os
# Paddleocr目前支持的多语言语种可以通过修改lang参数进行切换
# 例如`ch`, `en`, `fr`, `german`, `korean`, `japan`
ocr = PaddleOCR(use_angle_cls=True, lang="en")  # need to run only once to download and load model into memory
img_path = './img_input/test004.jpg'

result = ocr.ocr(img_path, cls=True)
for idx in range(len(result)):
    res = result[idx]
    for line in res:
        print(line)

# 显示结果
from PIL import Image
result = result[0]
image = Image.open(img_path).convert('RGB')
boxes = [line[0] for line in result]
# print("*********",boxes)
txts = [line[1][0] for line in result]
scores = [line[1][1] for line in result]
im_show = draw_ocr(image, boxes, txts, scores, font_path='./StyleText/fonts/en_standard.ttf')
im_show = Image.fromarray(im_show)
im_show.save('./ppocr_imgs_test/result.jpg')
