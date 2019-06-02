"""This module is a recursive function that prints out every nested
item on a single line, no matter how deeply it is nested. It also has the option for identation, that puts every nested list items few tabs in front of other items"""

def print_lol(the_list, indent=False, level=0):
    """It starts iteration and checks if the current list item is a
list. If it is a list, the function occures again on that item etc... If it is a single item, then it is printed on a single line. If the switch indent is set to True, the indentation is turned on and will be present, if not or if default is set (parameter not given), there will be no indentation"""
    for each_item in the_list:
        if isinstance (each_item, list):
            print_lol(each_item, indent, level+1)
        else:
            if indent==True:
                for tab_space in range(level):
                    print("\t", end='')
            print(each_item)
