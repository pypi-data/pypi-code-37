import os
from PIL import Image

def summarise(args):
    print(f"Summary of images")
    if args.no_color:
        separator_string = f"{'-'*20} "
    else:
        separator_string = f"\033[1;36;40m{'-'*20} "
    print(separator_string)

    for root,dirs,files in os.walk(args.dir):
        if root.count(os.path.sep) >= args.depth:
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
            if args.no_color:
                print(root)
                print_shape_dict(shapes)
                print(f" Total:\t\t{sum(shapes.values())}")
            else:
                print("\033[0;30;42m"+root+"\033[0;33;40m")
                print_shape_dict_color(shapes)
                print(f" \033[1;31;40mTotal:\t\t\033[00m {sum(shapes.values())}")
            print(separator_string)

def print_shape_dict_color(shapes):
    for k,v in shapes.items():
        print(f"\033[0;33;40m {k}:\t\033[00m {v}", end='\n')

def print_shape_dict(shapes):
    for k,v in shapes.items():
        print(f"{k}:\t{v}", end='\n')
