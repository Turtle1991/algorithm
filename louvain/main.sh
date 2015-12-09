#!/bin/bash

cd `dirname $0`
source ../common.sh
msg 'Process Start.'

dirUserRelationship=$DIR_RES/_userRelationship
dirLouvainData=$DIR_RES/_user_community_louvain

mkdir -p $dirLouvainData

cat $dirUserRelationship/$dateLast.txt | awk '{print $2"\t"$3"\t"$4}' > $dirLouvainData/$dateLast.txt

/usr/bin/python2.6 $DIR_SCRIPT/do.py $dirLouvainData/ $dateLast.txt

msg '结果导入数据表中'
query 'truncate table user_community_status_louvain'
load $dirLouvainData/community_status.txt user_community_status_louvain
query 'truncate table user_community_louvain'
load $dirLouvainData/community_result.txt user_community_louvain
