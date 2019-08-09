# Author: Wenfeng Du
# Create Date: 2019-08-01
# Description: 基于百度的人工智能API，把图片识别成文字，
#              并把相应的营养成分信息提取出来，保存到数据库。
# -*- coding: utf-8 -*-

from DataProcess import DataProcess
from AILogic import AILogic

get_filename = 'scm_ProductQRCode_piclinks.xlsx'
client_id = 'XXXXXXXXXXXXXXXXXXXX'
client_secret = 'XXXXXXXXXXXXXXXXXXXXX'
save_table = 'scm_nutrition_ocr'

if __name__ == '__main__':
    dp = DataProcess()
    df = dp.get_from_excel(get_filename)
    ai = AILogic()
    access_token = ai.get_baidutoken(client_id,client_secret)
    df = df.apply(ai.ocr_action, axis=1)
    dp.save_to_db(df,save_table)


