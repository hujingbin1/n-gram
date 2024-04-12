# import re

symbol = ',.!?。，？！'

# 语料库类
class Corpus(object):
    def __init__(self):
        self.content = ''
        self.size = 0

    # 导入语料库
    def loadcorpus(self, path):
        with open(path, 'r', encoding='utf-8', errors='ignore') as file:
            self.content = str(file.readlines())
            print(self.content)
            self.size = len(self.content)

# n-gram模型
class N_gram(object):
    def __init__(self, N, corpus):
        self.N = N
        self.corpus = corpus.content
        self.prob_list = []

    # 计算句子出现的概率
    def ComputeProb(self, endlist):
        for sen in endlist:
            lst = sen.split(" ")
            lens = len(lst)
            prob = 1.0

            if self.N > 1:
                prob *= (self.corpus.count(lst[0]) + 1) / (2*len(self.corpus))  # 加1平滑法
                for i in range(1, len(lst)):
                    strh = ''
                    stra = ''
                    k = 0
                    if i <= self.N:
                        k = 0
                    else:
                        k = i - self.N
                    for j in range(k, i):  # 找到前面的n个历史
                        strh += lst[j] + ' '
                    stra = strh + lst[i]
                    prob *= (self.corpus.count(stra) + 1) / (2*len(self.corpus))

            else:
                for i in range(len(lst)):
                    prob *= (self.corpus.count(lst[i]) + 1) / (2*len(self.corpus))

            self.prob_list.append(prob)
        print(dict(zip(endlist, self.prob_list)))

    # 找到最大概率的分法
    def findBiggestPro(self, endlist):
        max = 0.0
        index = 0
        for i in range(len(self.prob_list)):
            if max < self.prob_list[i]:
                max = self.prob_list[i]
                index = i
        print([str(endlist[index]), max])
        return str(endlist[index]), max

    def clearplst(self):
        self.prob_list.clear()

# 分词部分
class Segmentation(object):
    def __init__(self, content, corpus):
        self.content = content
        self.endlist = []
        self.endindex = 0
        self.worddict = corpus.content
        self.n_gram = N_gram(2, corpus)

    def processSeg(self):
        strA = ''
        seg_suc_str = ''
        prob_suc = 1.0
        global symbol
        # 开始进行切分
        for word in self.content:
            if word in symbol:
                self.endlist.clear()
                self.endindex = 0
                self.n_gram.clearplst()
                self.findAllSentence(strA)  # 列出切分后可能的句子
                # 计算所有句子概率
                if len(strA) > 1:
                    self.n_gram.ComputeProb(self.endlist)
                    strA, prob = self.n_gram.findBiggestPro(self.endlist)
                    prob_suc *= prob
                if strA != '':  # 当不是字符或单个字符多加个空格用于标示切分
                    strA += ' '
                seg_suc_str += strA + word + ' '
                strA = ''
                prob = 0
            elif word not in '\n\t\r':
                strA += word
        return seg_suc_str, prob_suc

    # 找出所有在语料库出现的字和词
    def findExistword(self, strA):
        if len(strA) <= 1:
            return
        exword = []
        for i in range(len(strA)):
            for j in range(i + 1, len(strA) + 1):
                if strA[i:j] in self.worddict:
                    exword.append([strA[i:j], i, j])
        print('exword is ', exword)
        return list(exword)

    # 找出所有可能出现的句子
    def findSentence(self, exword, strs, i, tlen):
        if self.endindex == tlen:
            self.endlist.append(strs)
            return
        else:
            for j in range(i + 1, len(exword)):
                if exword[i][2] == exword[j][1]:
                    strs1 = strs + ' ' + exword[j][0]
                    self.endindex = exword[j][2]
                    self.findSentence(exword, strs1, j, tlen)

    # 找出该句子的所有不同分词方式
    def findAllSentence(self, strA):
        exword = self.findExistword(strA)
        if exword != [] and exword != None:
            for i in range(len(exword)):
                if exword[i][1] == 0:
                    self.endindex = 0
                    strs = exword[i][0]
                    self.findSentence(exword, strs, i, len(strA))
            print('endlist is', self.endlist)

def main():
    # path = '..\\dataset\\news_tensite_xml.smarty.dat'
    path = './data.csv'
    corpus = Corpus()
    corpus.loadcorpus(path)

    seg_str = "我喜欢学习统计计算语言学我喜欢听吴老师讲课!"
    segmentation = Segmentation(seg_str, corpus)
    seg_suc_str, prob_suc = segmentation.processSeg()

    print(seg_suc_str, prob_suc)

if __name__ == '__main__':
    main()
