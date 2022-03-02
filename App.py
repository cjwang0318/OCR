# conda install flask
from flask import Flask, request
from flask import url_for
from opencc import OpenCC
from OCR import OCR_Kernel
from paddleocr import PaddleOCR
import os


class web_server:

    def __init__(self):
        # create app
        self.app = Flask(__name__)
        # OCR model path
        server_det_path = "./OCR_Model/ch_ppocr_server_v2.0_det/ch_ppocr_server_v2.0_det_infer"
        server_rec_path = "./OCR_Model/ch_ppocr_server_v2.0_rec/ch_ppocr_server_v2.0_rec_infer"

        # web api setting
        self.app.add_url_rule('/status', view_func=self.sendStatus, methods=['GET'])
        self.app.add_url_rule('/getResult', view_func=self.getResult, methods=['POST'])
        # self.app.add_url_rule('/image/query', view_func=self.queryImg, methods=['GET'])

        # init core
        #self.ocr = PaddleOCR(use_angle_cls=True, lang="ch")  # original mobil model
        self.ocr = PaddleOCR(use_angle_cls=True, lang='ch', use_gpu=True, rec_model_dir=server_rec_path)  # sever model
        # record status
        self.status = "free"
        self.failCode = ['1', '2', '3', '4', '5']

        # run flask
        self.app.run(host='0.0.0.0', port=5000, threaded=False)

    def sendStatus(self):  # 確認server的狀態
        answer = {"status": self.status}
        return answer

    def convert_tw2s(self, str):
        cc = OpenCC('tw2s')  # convert from Simplified Chinese to Traditional Chinese
        converted = cc.convert(str)
        return converted

    def getResult(self):  # 呼叫文案生成API
        # change status
        self.status = "processing"

        # decode json
        content = request.json
        img_b64code = content['image']
        answer = OCR_Kernel.getResult(self.ocr, img_b64code)

        # change status
        self.status = "free"
        return answer


if __name__ == '__main__':
    wbs = web_server()
