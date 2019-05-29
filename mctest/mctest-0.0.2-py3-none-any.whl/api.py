#!/usr/bin/env python
# encoding: utf-8
# @Time    : 2019/5/28 下午2:53

__author__ = 'Miracle'

from requests import request


class API:
    def __init__(self, host='http://test.magcore.clawit.com'):
        self._host = host
        self._links = {
            'NEW_GAME': (f'{self._host}/api/game', 'POST'),
            'GET_GAME_LIST': (f'{self._host}/api/game', 'GET'),
            'JOIN_GAME': (f'{self._host}/api/game', 'PATCH'),
            'START_GAME': (f'{self._host}/api/game/', 'PUT'),
            'GET_GAME': (f'{self._host}/api/game/', 'GET'),
            'REG_PLAYER': (f'{self._host}/api/player', 'POST'),
            'GET_PLAYER': (f'{self._host}/api/player/', 'GET'),
            'GET_MAP': (f'{self._host}/api/map/', 'GET'),
            'ATTACK_CELL': (f'{self._host}/api/cell/', 'PUT'),
        }
        self._headers = {
            'Content-Type': 'application/json',
            'Cache-Control': 'no-cache',
            'User-Agent': 'User-Agent:Mozilla/5.0'
        }

    def new_game(self, map_name):
        '''
        新建游戏房间，但不会自动加入

        :param map_name: 地图名称，目前地图支持：RectSmall, RectMid, RectLarge, RectPhone,

        response:
        Status Code: 200

        主推RectPhone，做了手机适配
        '''

        if not isinstance(map_name, (str,)):
            raise TypeError(f'map_name should be str, now {type(map_name)}')

        payload = {
            'Map': map_name
        }
        res = request(self._links['NEW_GAME'][1], self._links['NEW_GAME'][0], json=payload, headers=self._headers)
        print(f'New game: {res.text}')
        return res

    def get_game_list(self):
        '''
        获取游戏列表

        response:
        [
            {
                "id": "ce71d669e4d141a298472591de92f8e6",
                "map": "RectSmall",
                "state": 0
            }
        ]
        '''
        res = request(self._links['GET_GAME_LIST'][1], self._links['GET_GAME_LIST'][0], headers=self._headers)
        print(f'games list: {res.text}')
        return res

    def join_game(self, gid, pid):
        '''
        加入游戏

        :param gid: 游戏ID
        :param pid: 玩家ID

        response：

        成功 Status Code: 200
        失败 Status Code: 403
        '''
        if not isinstance(gid, (int,)):
            raise TypeError(f'gid should be int, now {type(gid)}')

        if not isinstance(pid, (int,)):
            raise TypeError(f'gid should be int, now {type(pid)}')

        payload = {
            'Game': gid,
            'Player': pid
        }
        res = request(self._links['JOIN_GAME'][1], self._links['JOIN_GAME'][0], json=payload, headers=self._headers)
        return res

    def start_game(self, gid):
        '''
        开始游戏

        :param gid: 游戏id

        response：
        成功 Status Code: 200
        失败 Status Code: 403
        '''
        if not isinstance(gid, (int,)):
            raise TypeError(f'gid should be int, now {type(gid)}')

        res = request(self._links['START_GAME'][1], self._links['START_GAME'][0] + gid, headers=self._headers)
        print(f'Start game {gid}: {res}')
        return res

    def get_game(self, gid):
        '''
        获取游戏详情

        :param gid: 游戏id

        response：
        {
            "Id": "ce71d669e4d141a298472591de92f8e6",
            "Map": "RectSmall",
            "State": 0,
            "Players": [
                {
                    "Index": 5,
                    "Color": 1,
                    "Name": "cc",
                    "State": 1
                }
            ],
            "Cells": [
                [{
                        "X": 0,
                        "Y": 0,
                        "Type": 0,
                        "State": 0,
                        "Owner": 0
                    },
                    {
                        "X": 1,
                        "Y": 0,
                        "Type": 1,
                        "State": 0,
                        "Owner": 0
                    }
                ],
                [{
                        "X": 0,
                        "Y": 1,
                        "Type": 1,
                        "State": 0,
                        "Owner": 0
                    },
                    {
                        "X": 1,
                        "Y": 1,
                        "Type": 0,
                        "State": 0,
                        "Owner": 0
                    }
                ]
            ]
        }
        '''

        if not isinstance(gid, (int,)):
            raise TypeError(f'gid should be int, now {type(gid)}')

        res = request(self._links['GET_GAME'][1], self._links['GET_GAME'][0] + gid, headers=self._headers)
        print(f'Get game {gid}: {res.status_code}')
        return res

    def reg_player(self, name, cid):
        '''
        注册玩家

        :param name: 玩家昵称
        :param cid: 玩家颜色，颜色值可选0-9

        response：
        {
            "Id": "784f7580cfba4344b039edecb8876dda",
            "Name": "Cola",
            "Token": "1e2e222bbca6493f9d5d740e9b70929b",
            "Energy": 0,
            "Color": 0,
            "State": 0,
            "Index": 2,
            "Bases": []
        }
        '''

        if not isinstance(name, (str,)):
            raise TypeError(f'name should be str, now {type(name)}')

        if not isinstance(cid, (int,)):
            raise TypeError(f'cid should be int, now {type(cid)}')

        payload = {
            'Name': name,
            'Color': cid
        }
        res = request(self._links['REG_PLAYER'][1], self._links['REG_PLAYER'][0], json=payload, headers=self._headers)
        print(f'Register player {name}: {res.json()["Id"]}')
        return res

    def get_player(self, pid):
        '''
        获取玩家信息

        :param pid: 玩家id

        response：
        {
            "Id": "784f7580cfba4344b039edecb8876dda",
            "Name": "Cola",
            "Token": "1e2e222bbca6493f9d5d740e9b70929b",
            "Energy": 0,
            "Color": 0,
            "State": 1,
            "Index": 2,
            "Bases": [
                "3,7"
            ]
        }
        '''

        if not isinstance(pid, (int,)):
            raise TypeError(f'pid should be int, now {type(pid)}')

        res = request(self._links['GET_PLAYER'][1], self._links['GET_PLAYER'][0] + pid, headers=self._headers)
        # print(f'Get player {pid}')
        return res

    def get_map(self, map_name):
        '''
        获取地图详情

        :param map_name: RectSmall, RectMid, RectLarge, RectPhone

        response:
        {
            "Edge": 4,
            "Shift": 0,
            "Direction": 0,
            "Rows": [
                "0111111111",
                "1000111111",
                "1011111111",
                "1111111111",
                "1111111111",
                "1111111111",
                "1111111111",
                "1111111101",
                "1111110001",
                "1111111110"
            ]
        }
        '''

        if not isinstance(map_name, (str,)):
            raise TypeError(f'map_name should be str, now {type(map_name)}')

        res = request(self._links['GET_MAP'][1], self._links['GET_MAP'][0] + map_name, headers=self._headers)
        print(f'Get map {map_name}')
        return res

    def attack_cell(self, gid, pid, x, y):
        '''
        攻击单元格

        :param gid: 游戏id
        :param pid: 玩家id
        :param x: x坐标
        :param y: y坐标

        response：
        成功 Status Code: 200
        失败 Status Code: 404
        '''

        if not isinstance(gid, (int,)):
            raise TypeError(f'gid should be int, now {type(gid)}')
        if not isinstance(pid, (int,)):
            raise TypeError(f'pid should be int, now {type(pid)}')
        if not isinstance(x, (int,)):
            raise TypeError(f'x should be int, now {type(x)}')
        if not isinstance(y, (int,)):
            raise TypeError(f'y should be int, now {type(y)}')

        payload = {
            "Game": gid,
            "Player": pid,
            "X": x,
            "Y": y
        }
        res = request(self._links['ATTACK_CELL'][1], self._links['ATTACK_CELL'][0], json=payload, headers=self._headers)
        # print(f'Attack cell <{x}, {y}>')
        return res
