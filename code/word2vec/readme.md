1. 以《武动乾坤》小说为数据集完成word2vec训练；

2. 模型选用gensim中的word2vec 或者 fasttext, 本次训练使用的是word2vec；但是fasttext对oov的词更友好;数据处理及训练相关代码见--word2vec_WDQK.ipynd文件

3. get_TSV.py 是通过embedding.txt 获取label.tsv 和 vector.tsv 文件的脚本，label.tsv 和 vector.tsv 文件可用于google的embedding projecter做展示

4. word2vec.model 是训练好的模型； word2vec_WDQK.wordvectors 是训练好的词向量和word的keyedvectors对象；embedding.txt是通过keyedvectors对象获取的dict对象