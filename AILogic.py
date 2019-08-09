# Author: Wenfeng Du
# Create Date: 2019-08-01
# -*- coding: utf-8 -*-

import urllib.request
import requests
import json
import base64
import re

class AILogic:
    """
    从百度AI的API解释图片并返回识别结果
    """

    def get_baidutoken(self, client_id, client_secret):
        """
        通过客户ID和客户密码获得token
        :param client_id:
        :param client_secret:
        :return:
        """
        # client_id 为官网获取的AK， client_secret 为官网获取的SK
        host = 'https://aip.baidubce.com/oauth/2.0/token?' + \
               'grant_type=client_credentials&client_id=' + client_id + '&client_secret=' + client_secret
        request = urllib.request.Request(host)
        request.add_header('Content-Type', 'application/json; charset=UTF-8')
        response = urllib.request.urlopen(request)
        content = response.read()
        access_token = json.loads(content)['access_token']
        self.access_token = access_token

    def img_tobase64(self, img_name):
        """
        图片转换成64位
        :param img_name:图片名称
        :return:
        """
        with urllib.request.urlopen(img_name) as f:
            base64_data = base64.b64encode(f.read())
            code64 = base64_data.decode()
        return code64

    def get_ocr_response(self, img_code, access_token):
        """
        OCR返回结果
        :param img_code:图片转码
        :param access_token: 访问token
        :return:
        """
        host = 'https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic?access_token=' + access_token
        datas = {'image': img_code}
        r = requests.post(host, data=datas)
        if r.status_code == 200:
            return r.content.decode('utf-8')
        else:
            return ""

    def ocr_action(self, df):
        """
        OCR结果提取文字
        :param df: 原始dataframe,按行取信息
        :return:
        """
        link = df['pic_links']
        if str(link) != 'nan' and len(link) > 0:
            link = link.split(',')[0]
            img_code = self.img_tobase64(link)
            response = self.get_ocr_response(img_code, self.access_token)
            jload = json.loads(response)
            words_result = jload['words_result']
            sentence = ""
            for i in range(len(words_result)):
                sentence += words_result[i]['words']
                df['sentence'] = sentence
            if "营养" in sentence:
                sentence = sentence.replace("O", '0')
                sentence = sentence.replace(" ","")
                searchObj = re.findall(r'每份?\(?(\d{1,3}[m|毫]?[9|g|l|克|升|L]?)\)?', sentence)
                if (len(searchObj) > 0):
                    df['nutrition_basic'] = searchObj[0]
                searchObj = re.findall(r'能量(\d{1,4})[k|千][J|焦|」]?', sentence)
                if (len(searchObj) > 0):
                    df['energy'] = searchObj[0]
                searchObj = re.findall(r'蛋白质(\d{1,3}\.?\d{0,2})[q|g|克]?', sentence)
                if (len(searchObj) > 0):
                    df['protein'] = searchObj[0]
                searchObj = re.findall(r'脂肪(\d{1,3}\.?\d{0,2})[a|g|q|克]?', sentence)
                if (len(searchObj) > 0):
                    df['fat'] = searchObj[0]
                searchObj = re.findall(r'反式脂肪酸(\d{1,3})[g|q|克]?', sentence)
                if (len(searchObj) > 0):
                    df['trans_fat'] = searchObj[0]
                searchObj = re.findall(r'碳水化合物(\d{1,3}\.?\d{0,2})[g|克]?', sentence)
                if (len(searchObj) > 0):
                    df['carbohydrate'] = searchObj[0]
                searchObj = re.findall(r'膳食纤维(\d{1,3}\.?\d{0,2})g?', sentence)
                if (len(searchObj) > 0):
                    df['fiber'] = searchObj[0]
                searchObj = re.findall(r'钠(\d{1,3})[m|毫]?[a|g|克]?', sentence)
                if (len(searchObj) > 0):
                    df['sodium'] = searchObj[0]
                searchObj = re.findall(r'左旋肉碱(\d{1,4})[m|毫]?[a|g|克]?', sentence)
                if (len(searchObj) > 0):
                    df['carnitine'] = searchObj[0]
        return df