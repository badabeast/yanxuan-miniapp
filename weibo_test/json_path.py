#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import ast


class HandleJson():
    def __init__(self, data):
        if data == None:
            print('请输入json格式数据')
            exit()

        if isinstance(data, str):
            try:
                self.data = ast.literal_eval(data)
            except:
                print('请输入正确的json格式数据')
                exit()
        elif isinstance(data, dict):
            self.data = data

    def __paths(self, data, path=''):
        '''
        用于遍历json树
        :param data: 原始数据，或者key对应的value值
        :param path: key值字符串，默认值为''
        :return:
        '''
        if isinstance(data, dict):
            for k, v in data.items():
                tmp = path + "['%s']" % k
                yield (tmp, v)
                yield from self.__paths(v, tmp)

        if isinstance(data, list):
            for k, v in enumerate(data):
                tmp = path + '[%d]' % k
                yield (tmp, v)
                yield from self.__paths(v, tmp)

    def find_key_path(self, key):
        '''
        查找key路径
        :param key: 需要查找路径的key值
        :return: 包含key值路径的list
        '''
        result = []
        for path, value in self.__paths(self.data):
            if path.endswith("['%s']" % key):
                result.append(path)
        # with open('path.txt', 'w+', encoding='utf-8') as f:
        #     list(map(lambda line: f.write(line + '\r'), result))
        return result

    def find_value_path(self, key):
        '''
        查找某个值的路径
        :param key: 需要查找的值，限制为字符串，数字，浮点数，布尔值
        :return:
        '''
        result = []
        for path, value in self.__paths(self.data):
            if isinstance(value, (str, int, bool, float)):
                if value == key:
                    result.append(path)
        # with open('path.txt', 'w+', encoding='utf-8') as f:
        #     list(map(lambda line: f.write(line + '\r'), result))
        # aaa = str("%s" % self.data + result[0])
        # print("aaa", aaa)

        return result


if __name__ == '__main__':
    data = {"b1": "1", "b2": {"b2_1": "ceshi", "b2_2": "要替换的"}}
    matcher='要替换的'
    new="替换后的"
    # data["b1"]=matcher
    # print(data)
    hj = HandleJson(data)
    res = hj.find_value_path(matcher)
    print(res)

