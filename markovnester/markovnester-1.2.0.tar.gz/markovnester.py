"""This module is a recursive function that prints out every nested
item on a single line, no matter how deeply it is nested"""

def print_lol(the_list, level=0):
    """It starts iteration and checks if the current list item is a
list. If it is a list, the function occures again on that item etc... If it is a single item, then it is printed on a single line"""
    for each_item in the_list:
        if isinstance (each_item, list):
            print_lol(each_item, level+1)
        else:
            for tab_space in range(level):
                print("\t", end='')
            print(each_item)
