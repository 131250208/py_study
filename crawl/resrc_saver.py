# -*- coding:utf-8 -*-

import os
import codecs
import zipfile
import crawl_wangpan007

def save_list(src_name,dir_path):
    src_list = []
    # extend_list
    src_list.extend(crawl_wangpan007.search_all(src_name))# wangpan007
    # 按热度排序

    # 分类存入资源并制作统一目录
    pass

# 打包目录为zip文件（未压缩）
def make_zip(source_dir, output_filename):
    zipf = zipfile.ZipFile(output_filename, 'w')
    pre_len = len(os.path.dirname(source_dir))
    for parent, dirnames, filenames in os.walk(source_dir):
        for filename in filenames:
            pathfile = os.path.join(parent, filename)
            arcname = pathfile[pre_len:].strip(os.path.sep)  # 相对路径
            zipf.write(pathfile, arcname)
    zipf.close()