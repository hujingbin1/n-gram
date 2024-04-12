import csv

#content语料建立字典
columns={}
#字典的索引
i = 0
# 获取多列的数据
with open('data.csv',encoding='utf-8') as csvfile:
    reader=csv.reader(csvfile)
    for row in reader:
      #读入content列的语料，用于建立语料库
        columns[i] = row[1]
        i = i+1
# print(columns)
#转成text文件并加上开始和结尾标志
with open("train.txt","w",encoding='utf-8') as f:                                             
    for i in range(1,len(columns)):                                                                 #对于双层列表中的数据
        # i = str(i).strip('[').strip(']').replace(',','').replace('\'','')+'\n'  #将其中每一个列表规范化成字符串
        f.write('<s>'+str(columns[i])+'</s>'+'\n')   