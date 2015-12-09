#!/usr/bin/python2.6
#-*- coding:utf-8 -*-

import math
import time
import sys
from pylouvain import PyLouvain

def do(path, source_data):
    start_time = time.time()
    print 'start time: ',start_time
    print 'louvain算法社团划分开始...'
    pyl = PyLouvain.from_file(path, source_data)
    partition, q = pyl.apply_method()
    # print partition
    out_file = open(path+"community_result.txt", 'w')

    #读取节点信息文件
    nodes_file = open(path+'nodes_tmp.txt', 'r')
    nodes_lines = nodes_file.readlines()
    nodes_file.close()
    nodes = {} #保存 节点序号-节点名称 信息
    for line in nodes_lines:
        n = line.split()
        if not n:
            break
        nodes[n[1]] = n[0]

    #社团信息 格式：标记 成员数
    print '统计社团信息 写入社团状态文件'
    community_status = open(path+'community_status.txt', 'w')
    i = 1
    label = {} # 格式 节点名称-社团标记
    for community in partition:
        community_status.write(str(i)+'\t'+str(len(community))+'\n') #社团标记 成员数
        #成员贴上社团标记
        for per in community:
            label[nodes[str(per)]] = str(i)
        i += 1
    community_status.close()

    #关联用户互动
    print '关联用户互动数据 写入结果文件'
    relationship_file = open(path+source_data, 'r')
    relationship_lines = relationship_file.readlines()
    relationship_file.close()
    for rela in relationship_lines:
        r = rela.split()
        if not r:
            break
        out_file.write('-\t'+r[0]+'\t'+label[r[0]]+'\t'+r[1]+'\t'+label[r[1]]+'\t'+r[2]+'\n')
    out_file.close()

    print 'end time: ',time.time()
    print '花费时间: ',(time.time()-start_time)/60,' min'

if __name__ == '__main__':
    do(sys.argv[1],sys.argv[2])
