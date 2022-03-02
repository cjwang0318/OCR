import os
import cv2
os.environ['KMP_DUPLICATE_LIB_OK']='True'
from paddleocr import PPStructure,draw_structure_result,save_structure_res

table_engine = PPStructure(show_log=True)

save_folder = './output/table'
#img_path = './ppocr_img/table/1.png'
#img_path = './ppocr_img/table/layout.jpg'
#img_path = './img_data/DKSH_img/sample/111.jpg' #file name English only
img_path = 'C:/cjwang/PycharmProjects/PaddleOCR/img_data/DKSH_img/sample/111.jpg'
img = cv2.imread(img_path)
result = table_engine(img)
save_structure_res(result, save_folder,os.path.basename(img_path).split('.')[0])

for line in result:
    line.pop('img')
    print(line)

from PIL import Image

font_path = 'C:/cjwang/PycharmProjects/PaddleOCR/img_data/ppocr_img/fonts/simfang.ttf'
image = Image.open(img_path).convert('RGB')
im_show = draw_structure_result(image, result,font_path=font_path)
im_show = Image.fromarray(im_show)
im_show.save('result.jpg')