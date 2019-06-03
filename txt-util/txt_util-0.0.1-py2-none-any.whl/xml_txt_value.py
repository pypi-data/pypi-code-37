# -*- coding: utf-8 -*-

def ele_value(minidom_ele):
    return minidom_ele.firstChild.nodeValue

def ele_value_from_dom(tag_name, dom_obj, index=0):
    return ele_value(dom_obj.getElementsByTagName(tag_name)[index]).replace('\n\n', '\n')