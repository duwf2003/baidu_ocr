# Author: Wenfeng Du
# Create Date: 2019-08-01
# -*- coding: utf-8 -*-

import pandas as pd
from sqlalchemy import create_engine

class DataProcess:
    """
    获取数据类
    """

    def get_from_excel(self, file_name):
        """
        从Excel获取图片识别数据
        :return:
        """
        df = pd.read_excel(file_name)
        return df

    def save_to_excel(self, df, file_name):
        """
        把数据从内存保存到Excel中
        :param df:
        :return:
        """
        writer = pd.ExcelWriter(file_name)
        writer.close()
        df.to_excel(writer, "OCR")
        writer.save()

    def save_to_db(self, df, save_table):
        mysql_engine = create_engine('mysql+pymysql://root:root123@XXX.XX.XX.XXX:3306/db_customer_level?charset=utf8')
        df.to_sql(save_table, con=mysql_engine, if_exists='append', index=False)

