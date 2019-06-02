#
# Copyright ⓒ2019 KSNU Info Lab.
# Dev. LEE DONGGUN(2019.05.07)
# 

"""
    # Last Update. 2019.05.07

    Ver. 19.05.071348
        - MSCOCO 폴더/파일 구분 없이 변환
        - 바이너리 마스트 데이터는 호환안됨.
        - 한번에 여러개의 annotation.json 데이터를 사용할 수 있도록 함.
"""

import os,sys,json
import numpy as np
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from deepgeo import Utils as utils
from deepgeo import Image

def update_loading_bar(num):
    sys.stdout.write("%s" % str(num))
    sys.stdout.flush()
    sys.stdout.write("\b" * len(str(num)))

def final_loading_bar():
    sys.stdout.write("\n")

def _mscoco_get_categories_(data):
    category= data['categories']
    categories={0:'bg'}
    sys.stdout.write(" > category : %d/1" % len(category))
    sys.stdout.flush()
    sys.stdout.write("\b")
    count=0
    for cate in category:
        count+=1
        update_loading_bar(count)
        categories.update({cate['id']:cate['name'].replace(" ","_").lower()})
    final_loading_bar()
    return categories

def _mscoco_get_images_(data, images_path):
    images = data['images']
    imgs = {}
    sys.stdout.write(" > image : %d/0" % len(images))
    sys.stdout.flush()
    sys.stdout.write("\b")
    count=0
    for image in images:
        count+=1
        update_loading_bar(count)
        img_id = image['id']
        img = Image(image['file_name'],images_path,[])
        imgs.update({img_id:img})
    final_loading_bar()
    return imgs

def _mscoco_add_annotations_(annotations, images, categories):
    sys.stdout.write(" > annotation : %d/0" % len(annotations))
    sys.stdout.flush()
    sys.stdout.write("\b")
    count =0
    f=0
    for annotation in annotations:
        count+=1
        update_loading_bar(count)

        segmentation = annotation['segmentation']
        if annotation['iscrowd'] == 1:
            f+=1
            continue
        temp={
            "areaInImage":{
                "type":"Polygon",
                "coordinates":segmentation
            },
            "annotationText":categories[annotation['category_id']]
        }
        images[annotation['image_id']].add_annotation(temp)
    final_loading_bar()
    return images, f

def _save_(images, create_json):
    sys.stdout.write(" > data to json : %d/0" % len(images))
    sys.stdout.flush()
    sys.stdout.write("\b")
    count =0 
    f = 0
    for idx in list(images.keys()):
        image = images[idx]
        count+=1
        update_loading_bar(count)
        if len(image.get_annotation()) == 0:
            f+=1
            continue
        path = create_json.replace(".json","")
        stphoto = image.to_stphoto()
        name = path+"_"+stphoto['uri']+".json"
        
        if os.path.isfile(name) is False:
            with open(name, 'w') as outfile:
                json.dump(stphoto, outfile, indent='\t', sort_keys=True, default=utils.default_DICT_TO_JSON)
        del stphoto
        del images[idx]
    final_loading_bar()
    print (" > image loss rate : ",(count - f)/count*100,"%")

def _mscoco_to_image_(mscoco, images_path=""):
    sys.stdout.write(mscoco+" Read JSON...")
    sys.stdout.flush()
    if isinstance(mscoco,str):
        with open(mscoco) as data_file:    
            data = json.load(data_file)
    else:
        data = mscoco
    sys.stdout.write("OK\n")
    sys.stdout.flush() 
    images = _mscoco_get_images_(data,images_path)
    categories = _mscoco_get_categories_(data)
    annotations = data['annotations']
    images, an_f = _mscoco_add_annotations_(annotations, images, categories)    
    print (" > annotation loss rate : ",(len(annotations) - an_f)/len(annotations)*100,"%")
    return images

def _is_it_(path):
    if os.path.isfile(path):
        return 1
    elif os.path.isdir(path):
        return 2
    else:
        return -1

def main(argv):
    if argv[0]=="help":
        print('"변환할 파일 혹은 폴더" "저장할 JSON 파일경로 및 명" "이미지 폴더"')
        print('"d:/instances/instances_val2018.json" "c:/annotation/stphoto.json" "d:/images"')
        print('"d:/instances" "c:/annotation/stphoto.json" "d:/images"')
        exit(1)
    c_input = _is_it_(argv[0])
    if c_input is -1:
        print("Input : A file or folder that does not exist.")
        exit(1)
    if argv[1].split(".json")[-1] != '':
        print("Output : It is not a JSON file.")
        exit(1)
    c_image_path = _is_it_(argv[2])
    if c_image_path != 2:
        print("Image path : It is not a Folder.")
        exit(1)
    images = {}
    if c_input == 1:
        images = _mscoco_to_image_(argv[0], argv[2])
    else:
        for path in os.listdir(argv[0]):
            folder = utils.create_folder(argv[0])
            images.update(_mscoco_to_image_(folder+path, argv[2]))
    _save_(images, argv[1])

if __name__ == "__main__":
    main(sys.argv[1:])