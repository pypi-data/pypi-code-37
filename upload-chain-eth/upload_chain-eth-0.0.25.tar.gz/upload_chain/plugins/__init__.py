#! /usr/bin/env python
# -*- coding: utf8 -*-
"""
Author:       yuyongpeng@hotmail.com
Github:       https://github.com/yuyongpeng/
Date:         2019-04-17 12:37:21
LastEditors:  
LastEditTime: 2019-04-17 12:37:21
Description:  
"""
from upload_chain.logger import logger
import toolz


class Processor(object):
    # 注册的组件
    """
    PLUGINS = {
        'notice': {
            'email': CLASS,     // 进行`email`通知处理
            'database': CLASS,  // 进行`database`通知处理
            'rabbitmq': CLASS,  // 进行`rabbitmq`队列通知处理
            'kafka': CLASS      // 进行`kafka`队列通知处理
        }
    }
    """
    PLUGINS = {}

    def process_notice(self, notice_name, body):
        """
        调用`notice`插件
        :param notice_name: 插件名称
        :param body: 需要处理的内容
        :return:
        """
        if 'notice' not in self.PLUGINS:
            logger.error("系统目前没有任何`notice`类型的插件, 请检查代码".format(notice_name))
        else:
            if notice_name not in self.PLUGINS['notice']:
                logger.error("{} 这个插件在`notice`类型中不存在, 请检查代码".format(notice_name))
            else:
                tag = self.PLUGINS['notice'][notice_name]()
                if hasattr(self.PLUGINS['notice'][notice_name], 'before'):
                    tag.before(body)

                tag.process(body)

                if hasattr(self.PLUGINS['notice'][notice_name], 'after'):
                    tag.after(body)

    @classmethod
    def plugin_register(cls, type=None):
        """
        注册插件的包装器
        :param type: 注册的类型
        :return:
        """
        if type is None:
            print('注册的event不能为空')
            exit(2)

        def wrapper(plugin):
            if 'notice' not in cls.PLUGINS:
                cls.PLUGINS.update({'notice': {type: plugin}})
            else:
                cls.PLUGINS['notice'].update({type: plugin})
            return plugin
        return wrapper
