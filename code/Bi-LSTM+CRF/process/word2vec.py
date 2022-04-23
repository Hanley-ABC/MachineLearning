from gensim.models.word2vec import Word2Vec
import jieba
import codecs

train_sentences = codecs.open('/code/Bi-LSTM+CRF/data/MSRA/train/train_sentences.txt', 'r', 'utf-8')
test_sentences = codecs.open('/code/Bi-LSTM+CRF/data/MSRA/test/test_sentences.txt', 'r', 'utf-8')

sentences = []
for sentence in train_sentences.readlines():
    sentence = sentence.strip('\n')
    word_cut = jieba.cut(sentence, cut_all=False)
    sentence_words = list(word_cut)
    sentences.append(sentence_words)
train_sentences.close()

for sentence in test_sentences.readlines():
    sentence = sentence.strip('\n')
    word_cut = jieba.cut(sentence, cut_all=False)
    sentence_words = list(word_cut)
    sentences.append(sentence_words)
test_sentences.close()

# min_count=1也是因为语料太少，否则低频词语会被滤掉
model = Word2Vec(sentences, vector_size=30, window=5, min_count=1, workers=4)
model.save('/Users/liuhy/workspace/NLP/code/MachineLearning/code/Bi-LSTM+CRF/models/word2vec.model')