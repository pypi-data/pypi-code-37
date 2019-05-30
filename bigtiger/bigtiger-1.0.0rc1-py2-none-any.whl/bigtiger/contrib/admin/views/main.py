# -*- coding: utf-8 -*-

'''
Created on 2014-5-18
@author: linkeddt.com
'''

from __future__ import unicode_literals

import json

from django.utils.safestring import mark_safe
from django.shortcuts import HttpResponseRedirect

from bigtiger.utils.tree import tree_sorted
from bigtiger.views.generic import TemplateResponseMixin, View, SysConfContextMixin, PermissionMixin


def menu_order(menus):
    return sorted(menus, key=lambda e: e['order_number'], reverse=False)


def gen_menu_tree(parent_menu, menus):
    parent_menu_id = parent_menu['id']
    parent_menu_depth = (parent_menu['depth'] or 0) + 1

    chlid_menus = [item for item in menus if item['parent_id']
                   == parent_menu_id and item['depth'] == parent_menu_depth]
    chlid_menus = menu_order(chlid_menus)

    if chlid_menus:
        parent_menu['childs'] = chlid_menus
        for item in chlid_menus:
            gen_menu_tree(item, menus)


class MainView(SysConfContextMixin, PermissionMixin, TemplateResponseMixin, View):
    template_name = "admin/main.htm"

    def get(self, request, *args, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)

        ps = self.get_session_permissions()
        if ps is None:
            return HttpResponseRedirect('/')

        ps = filter(lambda item: item['status'] == 1, ps)

        root_menu = [item for item in ps if item['parent_id'] is None].pop()
        gen_menu_tree(root_menu, ps)

        cols = self.gen_menu_cols(ps, 15)
        context['root_menu'] = root_menu
        context['menusJson'] = mark_safe(json.dumps(root_menu))
        context['cols'] = cols
        return self.render_to_response(context)

    def gen_menu_cols(self, ps, col_count=12):
        """ 构建菜单清单中的菜单数据，用于模板的显示
        """
        lst = tree_sorted(ps, key=lambda item: item['order_number'], join=lambda item,
                          parent_item: item['parent_id'] == parent_item['id'])
        lst = filter(lambda item: item['depth'] < 4, lst)

        cols, col, index, line, mainId = [], None, 0, None, None
        for item in lst:
            if index % col_count == 0:
                col = []
                cols.append(col)

            depth = item['depth']

            if depth == 1:
                mainId = item['id']

            if depth == 2:
                line = item
                line['children'] = []
                col.append(line)
            elif depth == 3:
                item['mainId'] = mainId
                line['children'].append(item)
            index = index + 1
        return cols
