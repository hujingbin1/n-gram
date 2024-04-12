from  LangModel import *
import re
# 导入模块
import csv
import pandas as pd

def tokenize(text):
  #将文本转换为小写并去除标点符号
  text = text.lower()
  text = re.sub(r'[^\w\s]'," ", text)
  #将文本分成单词列表
  words = text.split()
  print(words)
  print()
  #创建bigram列表
  bigrams = []
  for i in range(len(words)-1):
    bigrams.append((words[i], words[i+1]))
  return bigrams

if __name__ == '__main__':
    actual_dataset = read_sentences_from_file("./train.txt")
    actual_dataset_test = read_sentences_from_file("./test.txt")
    actual_dataset_model_smoothed = BigramLanguageModel(actual_dataset, smoothing=True)
    print("---------------- Actual dataset ----------------\n")
    print("PERPLEXITY of train.txt")
    print("unigram: ", calculate_unigram_perplexity(actual_dataset_model_smoothed, actual_dataset))
    print("bigram: ", calculate_bigram_perplexity(actual_dataset_model_smoothed, actual_dataset))

    print("")

    print("PERPLEXITY of test.txt")
    print("unigram: ", calculate_unigram_perplexity(actual_dataset_model_smoothed, actual_dataset_test))
    print("bigram: ", calculate_bigram_perplexity(actual_dataset_model_smoothed, actual_dataset_test))