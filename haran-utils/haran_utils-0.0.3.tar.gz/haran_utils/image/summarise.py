import os
from PIL import Image

def summarise(args):
    print(f"Summary of images")
    separator_string = f"\033[1;36;40m{'-'*10} "
    print(separator_string)
    dir = args.dir
    depth = args.depth
    for root,dirs,files in os.walk(dir):
        if root.count(os.path.sep) >= depth:
            del dirs[:]
        shapes = {}
        for item in files:
            item_path = os.path.join(root,item)
            if os.path.isfile(item_path):
                try:
                    shape = Image.open(item_path).size
                except OSError:
                    pass
                else:
                    if shape not in shapes.keys():
                        shapes[shape] = 1
                    else:
                        shapes[shape] +=1
        if shapes == {}:
            #print("No images found")
            pass
        else:
            print("\033[0;30;42m"+root+"\033[0;33;40m")
            # print(shapes)
            print_shape_dict(shapes)
            print(f"\033[1;31;40mTotal: \033[00m {sum(shapes.values())}")
            print(separator_string)

def print_shape_dict(shapes):
    for k,v in shapes.items():
        print(f"\033[0;33;40m {k}: \033[00m {v}", end='\n')
    # print()
