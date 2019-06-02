#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  @file     models/base.py
#  @author   kaka_ace <xiang.ace@gmail.com>
#  @date
#  @brief
#
from sqlalchemy.ext.declarative import (
    declarative_base,
    DeclarativeMeta,
)
from sqlalchemy.orm import aliased
# 元类
class ModelMeta(DeclarativeMeta):
    def __new__(cls, name, bases, d):
        return DeclarativeMeta.__new__(cls, name, bases, d)
    def __init__(self, name, bases, d):
        DeclarativeMeta.__init__(self, name, bases, d)
#
_Base = declarative_base(metaclass=ModelMeta)
class BaseModel(_Base):
    __abstract__ = True
    # 基类的 _column_name_sets  是为实现的类型
    _column_name_sets = NotImplemented
    def to_dict(self):
        """
        """
        return dict(
            (column_name, getattr(self, column_name, None)) \
                for column_name in self._column_name_sets
        )
    @classmethod
    def get_column_name_sets(cls):
        """
        获取 column 的定义的名称(不一定和数据库字段一样)
        """
        return cls._column_name_sets
    __str__ = lambda self: str(self.to_dict())
    __repr__ = lambda self: repr(self.to_dict())
def modelmeta__new__(cls, name, bases, namespace, **kwds):
    column_name_sets = set()
    for k, v in namespace.items():
        if getattr(v, '__class__', None) is None:
            continue
        if v.__class__.__name__ == 'Column':
            column_name_sets.add(k)
    # obj = type.__new__(cls, name, bases, dict(namespace))
    obj = DeclarativeMeta.__new__(cls, name, bases, dict(namespace))
    # update set
    obj._column_name_sets = column_name_sets
    return obj
# modify BaseModel' metatype ModelMeta' __new__ definition
setattr(ModelMeta, '__new__', modelmeta__new__)