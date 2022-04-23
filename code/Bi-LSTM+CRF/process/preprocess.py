import codecs
import re
import jieba

from gensim.models import Word2Vec


class Preprocess:

    # 重新调整训练集和测试集
    def build_train_test(self, origion_train, origion_test, train, test):
        origion_train_data = codecs.open(origion_train, 'r', 'utf-8')
        origion_test_data = codecs.open(origion_test, 'r', 'utf-8')

        train_data = codecs.open(train, 'w', 'utf-8')
        test_data = codecs.open(test, 'w', 'utf-8')

        for line in origion_train_data.readlines():
            train_data.write(line)
        origion_train_data.close()

        split_num = 4266
        i = 1
        for line in origion_test_data.readlines():
            if i < split_num:
                train_data.write(line)
            else:
                test_data.write(line)
            i += 1
        origion_test_data.close()
        train_data.close()
        test_data.close()

    # 将训练集和测试集中的每个字做标注
    def build_word_tag(self, origion_data_path, word_tag_path):
        origion_data = codecs.open(origion_data_path, 'r', 'utf-8')
        word_tag = codecs.open(word_tag_path, 'w', 'utf-8')
        tags = set('o')
        for line in origion_data.readlines():
            line = line.strip().split()
            if len(line) == 0:
                continue
            for word in line:
                word = word.split('/')
                if word[1] != 'o':
                    if len(word[0]) == 1:
                        word_tag.write(word[0] + "/B_" + word[1] + " ")
                        tags.add('B_' + word[1])
                    else:
                        word_tag.write(word[0][0] + "/B_" + word[1] + " ")
                        for j in word[0][1:len(word[0])]:
                            word_tag.write(j + "/I_" + word[1] + " ")
                        tags.add('B_' + word[1])
                        tags.add('I_' + word[1])
                else:
                    for j in word[0]:
                        word_tag.write(j + "/o" + " ")
            word_tag.write('\n')

        origion_data.close()
        word_tag.close()

        return list(tags)

    # 将训练集和测试集转换成句子和标签的序列
    def build_sentences_labels(self, word_tag_path, sentences_path, labels_path, tag2id):
        word_tag = codecs.open(word_tag_path, 'r', 'utf-8')
        sentences = codecs.open(sentences_path, 'w', 'utf-8')
        labels = codecs.open(labels_path, 'w', 'utf-8')

        for line in word_tag.readlines():
            line = re.sub('[。；！：？、‘’“”●《》（）……『』]/[o]', '', line)
            line = line.strip('\n')
            chars_tags = line.split(' ')
            sentence = []
            label = []
            for char_tag in chars_tags:
                if char_tag != '':
                    char_tag = char_tag.split('/')
                    char = char_tag[0]
                    tag = char_tag[1]
                    if char != '，':
                        sentence.append(char)
                        label.append(tag2id[tag])
                    else:
                        sentences.write(''.join(sentence) + '\n')
                        labels.write(''.join(map(lambda x: str(x), label)) + '\n')
                        sentence = []
                        label = []

        word_tag.close()
        sentences.close()
        labels.close()

    # 将训练集和测试集中的字和词全部取出来编号
    def build_word_char_number(self, sentences_path, word_number_path, char_number_path):
        sentences = codecs.open(sentences_path, 'r', 'utf-8')
        char_number = codecs.open(char_number_path, 'w', 'utf-8')
        word_number = codecs.open(word_number_path, 'w', 'utf-8')

        all_chars = []
        all_words = []
        for sentence in sentences.readlines():
            sentence = sentence.strip('\n')
            sentence_chars = list(sentence)
            word_cut = jieba.cut(sentence, cut_all=False)
            sentence_words = list(word_cut)
            all_chars.extend(sentence_chars)
            all_words.extend(sentence_words)

        all_chars = list(set(all_chars))
        all_words = list(set(all_words))

        for i in range(len(all_chars)):
            char_number.write(all_chars[i] + ':' + str(i + 1) + '\n')

        for i in range(len(all_words)):
            word_number.write(all_words[i] + ':' + str(i + 1) + '\n')

        sentences.close()
        char_number.close()
        word_number.close()

    # 因为测试集中的字必须出现在训练集中，否则没有匹配的字向量，这里过滤掉训练集中没有的字所在的句子
    def filter_test_sentences_labels(self, train_char_number_path, test_sentences_path, test_labels_path,
                                     test_sentences_filter_path, test_labels_filter_path):
        train_char_list = []
        train_char_number_data = codecs.open(train_char_number_path, 'r', 'utf-8')
        for line in train_char_number_data.readlines():
            line = line.strip().split(':')
            train_char_list.append(line[0])
        train_char_number_data.close()

        test_sentences_list = []
        test_sentences_data = codecs.open(test_sentences_path, 'r', 'utf-8')
        for line in test_sentences_data.readlines():
            line = line.strip()
            test_sentences_list.append(line)
        test_sentences_data.close()

        test_labels_list = []
        test_labels_data = codecs.open(test_labels_path, 'r', 'utf-8')
        for line in test_labels_data.readlines():
            test_labels_list.append(line)
        test_labels_data.close()

        test_sentences_filter_data = codecs.open(test_sentences_filter_path, 'w', 'utf-8')
        test_labels_filter_data = codecs.open(test_labels_filter_path, 'w', 'utf-8')
        for i in range(len(test_sentences_list)):
            flag = True
            sentence = test_sentences_list[i]
            label = test_labels_list[i]
            chars = list(sentence)
            for char in chars:
                if char not in train_char_list:
                    flag = False
                    break
            if flag:
                test_sentences_filter_data.write(sentence + '\n')
                test_labels_filter_data.write(label)
        test_sentences_filter_data.close()
        test_labels_filter_data.close()

    # 统计字的个数，生成词向量矩阵、字与编号的字典、词与编号的字典
    def get_paras(self, train_char_number_path, train_word_number_path, test_word_number_path, word2vec_model):
        num_chars = 0
        char_number_dict = {}
        train_char_number_data = codecs.open(train_char_number_path, 'r', 'utf-8')
        for line in train_char_number_data.readlines():
            num_chars += 1
            line = line.strip('\n')
            char_number = line.split(':')
            char = char_number[0]
            number = int(char_number[1])
            char_number_dict[char] = number
        train_char_number_data.close()

        words = []
        train_word_number_data = codecs.open(train_word_number_path, 'r', 'utf-8')
        for line in train_word_number_data.readlines():
            line = line.strip('\n')
            word_number = line.split(':')
            word = word_number[0]
            words.append(word)
        train_word_number_data.close()

        test_word_number_data = codecs.open(test_word_number_path, 'r', 'utf-8')
        for line in test_word_number_data.readlines():
            line = line.strip('\n')
            word_number = line.split(':')
            word = word_number[0]
            words.append(word)
        test_word_number_data.close()

        words = list(set(words))
        word_embeddings = []
        word_number_dict = {}
        i = 1
        for word in words:
            word_embeddings.append(word2vec_model.wv.get_vector(word))
            word_number_dict[word] = i
            i += 1

        return num_chars, word_embeddings, char_number_dict, word_number_dict

    # 生成句子的字的编号向量、词的编号向量，句子的标签向量
    def get_model_seq(self, char_number_dict, word_number_dict, sentences_path, labels_path, seq_len):
        def padding(vec):
            if len(vec) >= seq_len:
                return vec[:seq_len]
            else:
                vec.extend([0] * (seq_len - len(vec)))
            return vec

        sentences_chars_vec = []
        sentences_words_vec = []
        sentences_data = codecs.open(sentences_path, 'r', 'utf-8')
        for line in sentences_data.readlines():
            line = line.strip('\n')
            chars = list(line)
            word_cut = jieba.cut(line, cut_all=False)
            words = list(word_cut)
            sentence_chars_vec = []
            for char in chars:
                sentence_chars_vec.append(char_number_dict[char])
            sentence_words_vec = []
            for word in words:
                word_chars = list(word)
                word_number = word_number_dict[word]
                for word_char in word_chars:
                    sentence_words_vec.append(word_number)
            sentences_chars_vec.append(padding(sentence_chars_vec))
            sentences_words_vec.append(padding(sentence_words_vec))
        sentences_data.close()

        sentences_labels = []
        labels_data = codecs.open(labels_path, 'r', 'utf-8')
        for label in labels_data.readlines():
            sentence_label = list(label.strip('\n'))
            sentence_label = list(map(lambda x: int(x), sentence_label))
            sentences_labels.append(padding(sentence_label))
        labels_data.close()

        return sentences_chars_vec, sentences_words_vec, sentences_labels

if __name__ == '__main__':
    tags = ['B_nr', 'o', 'I_nr', 'I_ns', 'I_nt', 'B_nt', 'B_ns']
    origion_train = '/Users/liuhy/workspace/NLP/code/MachineLearning/code/Bi-LSTM+CRF/data/MSRA/train1.txt'
    origion_test = '/Users/liuhy/workspace/NLP/code/MachineLearning/code/Bi-LSTM+CRF/data/MSRA/testright1.txt'
    train = '/Users/liuhy/workspace/NLP/code/MachineLearning/code/Bi-LSTM+CRF/data/MSRA/train/train.txt'
    test = '/Users/liuhy/workspace/NLP/code/MachineLearning/code/Bi-LSTM+CRF/data/MSRA/test/test.txt'

    train_word_tag = '/Users/liuhy/workspace/NLP/code/MachineLearning/code/Bi-LSTM+CRF/data/MSRA/train/train_word_tag.txt'
    test_word_tag = '/Users/liuhy/workspace/NLP/code/MachineLearning/code/Bi-LSTM+CRF/data/MSRA/test/test_word_tag.txt'

    train_sentences_path = '/code/Bi-LSTM+CRF/data/MSRA/train/train_sentences.txt'
    train_label_path = '/code/Bi-LSTM+CRF/data/MSRA/train/train_labels.txt'
    test_sentences_path = '/code/Bi-LSTM+CRF/data/MSRA/test/test_sentences.txt'
    test_label_path = '/code/Bi-LSTM+CRF/data/MSRA/test/test_labels.txt'

    train_word_vocabulary = '/Users/liuhy/workspace/NLP/code/MachineLearning/code/Bi-LSTM+CRF/data/MSRA/train/train_word_vocabulary.txt'
    train_char_vocabulary = '/Users/liuhy/workspace/NLP/code/MachineLearning/code/Bi-LSTM+CRF/data/MSRA/train/train_char_vocabulary.txt'
    test_word_vocabulary = '/Users/liuhy/workspace/NLP/code/MachineLearning/code/Bi-LSTM+CRF/data/MSRA/test/test_word_vocabulary.txt'
    test_char_vocabulary = '/Users/liuhy/workspace/NLP/code/MachineLearning/code/Bi-LSTM+CRF/data/MSRA/test/test_char_vocabulary.txt'

    test_sentences_filter_path = '/code/Bi-LSTM+CRF/data/MSRA/test/test_sentences_filter.txt'
    test_labels_filter_path = '/code/Bi-LSTM+CRF/data/MSRA/test/test_labels_filter.txt'

    # build_train_test(origion_train, origion_test, train, test)
    # build_word_tag(train, train_word_tag)
    # build_word_tag(test, test_word_tag)

    tag2id = dict([(value, index) for index, value in enumerate(tags)])

    # build_sentences_labels(train_word_tag, train_sentences_path, train_label_path, tag2id)
    # build_sentences_labels(test_word_tag, test_sentences_path, test_label_path, tag2id)

    # build_word_char_number(train_sentences_path, train_word_vocabulary, train_char_vocabulary)

    # filter_test_sentences_labels(train_char_vocabulary, test_sentences_path, test_label_path, test_sentences_filter_path, test_labels_filter_path)

    # build_word_char_number(test_sentences_filter_path, test_word_vocabulary, test_char_vocabulary)

    # word2vec_model = Word2Vec.load('/Users/liuhy/workspace/NLP/code/MachineLearning/code/Bi-LSTM+CRF/models/word2vec.model')
    #
    # num_chars, word_embeddings, char_number_dict, word_number_dict = get_paras(train_char_vocabulary,
    #                                                                            train_word_vocabulary,
    #                                                                            test_word_vocabulary,
    #                                                                            word2vec_model)
    # sentences_chars_vec, sentences_words_vec, sentences_labels = get_model_seq(char_number_dict,
    #                                                                            word_number_dict,
    #                                                                            train_sentences_path,
    #                                                                            train_label_path,
    #                                                                            seq_len=30)
