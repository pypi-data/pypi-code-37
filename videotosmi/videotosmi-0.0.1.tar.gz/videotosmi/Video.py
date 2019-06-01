from scipy import ndimage
import os
import cv2
from SMI import SMI
import deepgeo

class Video:
    def __init__(self):
        self.engine = deepgeo.Engine()

    def add_model(self, model_name, lib_name, config_data):
        self.engine.add_model(model_name, lib_name, config_data)

    def arr_to_text(self, r, model_name, ftr=None):
        data = self.arr_count(r, model_name,ftr)
        str_data = ""
        for key in sorted(data.keys()):
            str_data += str(key) + " : " + str(data[key]) + "  "
        return str_data

    def arr_count(self, r, model_name, ftr=None):
        data = {}
        for id in r['class_ids']:
            key = self.engine.get_config(model_name,'CATEGORY')[id]
            check = False
            if ftr is None:
                check = True
            else:
                if key in ftr or len(ftr) == 0:
                    check = True
            if check is True:
                if key in data.keys():
                    data[key] += 1
                else:
                    data.update({key: 1})
        return data

    def detect(self, file_url, model_name, frame_set=None, rotation=90, ftr=[]):
        assert model_name in self.engine.get_model_list(), "등록되지 않은 model 이름입니다."
        assert os.path.isfile(file_url), "파일이 존재하지 않습니다."

        print(file_url + " 파일의 SMI 변환 과정을 시작합니다.")

        cap = cv2.VideoCapture(file_url)
        frame_rate = int(cap.get(5))
        if frame_set is None:
            frame_set = frame_rate
        print("Frame Rate : " + str(frame_rate))
        print("Frame Set : " + str(frame_set))
        file_url = file_url.replace("\\","/")
        file_ext = file_url.split("/")[-1].split(".")[-1]
        smi = SMI(file_url.split("."+file_ext)[0])
        if (cap.isOpened() == False):
            print("Error opening video stream or file")
        frame_num = 0
        frame_sec = (1000 * frame_set) / frame_rate
        sec = 0
        while (cap.isOpened()):
            ret, frame = cap.read()
            if ret is True:
                if frame_num % frame_set == 0:
                    frame = ndimage.rotate(frame, rotation)
                    print("작업 : " + str(int((sec+frame_sec)/1000)) + "s")
                    r = self.engine.detect(model_name, [frame])[0][0]
                    smi.insert(self.arr_to_text(r, model_name, ftr), int(sec))
                    sec += frame_sec
            else:
                break
            frame_num += 1
        cap.release()
        cv2.destroyAllWindows()
        del smi

        print(file_url + " 파일의 SMI 변환 과정을 종료합니다.")
        print(file_url.split("."+file_ext)[0] + ".smi 으로 추출되었습니다.")