from pyltp import Segmentor
import os
import math

# Set your own model path 设置模型路径
MODELDIR = "/vagrant/software/ltp_data_v3.4.0"

class LtpProcess(object):
    """创建一个类，用来进行NLP的分词处理。

    Attributes:
                content: 要处理的文本内容

    """

    def __init__(self, content):
        self.content = content

    def ltp_word(self):
        """创建一个方法，用来进行句子的分词、词性分析等处理。"""
        # 分词
        segmentor = Segmentor()
        segmentor.load(os.path.join(MODELDIR, "cws.model"))
        words = segmentor.segment(self.content)

        segmentor.release()

        return words

#  函数:给定一个词组列表和一个字符串，查找字符串中是否含有词组列表的任何组合，并返回权重
class StringSortWeight(object):
    """函数:给定一个词组列表和一个字符串，查找字符串中是否含有词组列表的任何组合，并返回权重.

    Attributes:
                content: 要处理的文本内容

    """
    def __init__(self, word_list, str_content):
        self.word_list = word_list
        self.str_content = str_content

    def word_join(self, begin_position, word_l):
        """创建一个方法，给定word_list中要连接字符串的起始位置和连接的次数，返回连接的字符串"""
        tmp_str = ''
        for x in range(word_l):
            tmp_str = self.word_list[begin_position] + tmp_str
            begin_position = begin_position + 1
        return tmp_str

    def weight(self):
        """创建一个方法，给定word_list中要连接字符串的起始位置和连接的次数，返回连接的字符串"""
        word_list_number = (len(self.word_list))
        sort_weight = 0  # 权重
        for word_int in range(word_list_number):
            word_long = word_list_number - word_int  # 从最长的词组组合长度word_list_number开始
            combination_number = word_int + 1  #  各种组合的可能性数量
            # 循环取得给定长度的所有词组组合,以词组组合在字符串中出现的次数，赋予其权重并对权重进行累加，返回最后总权重
            for begin_str in range(combination_number):
                tmp_word_str = self.word_join(begin_str, word_long)
                integration = self.str_content.count(tmp_word_str)
                if integration > 0:  # 若词组组合在字符串中出现的次数大于0
                    sort_weight = pow(integration, 5) + 10*integration + sort_weight

        return sort_weight


def group_by(one_list, kk, re):

    one_list.sort(key=lambda s: s[kk], reverse = False)  # 按第kk列升序排序

    ll = len(one_list)
    # [[关键字权重，讲稿ID]，[......].......]
    dk_list = [[]]
    dk_list[0].append(one_list[0][re])
    dk_list[0].append(one_list[0][kk])
    wwt = 0
    for rt in range(ll):
        if rt == 0:
            pass
        elif one_list[rt][1] == one_list[rt-1][1]:
            dk_list[wwt][0] = dk_list[wwt][0] + one_list[rt][0]
        elif one_list[rt][1] != one_list[rt-1][1]:
            wwt = wwt + 1
            dk_list.append([])
            dk_list[wwt].append(one_list[rt][0])
            dk_list[wwt].append(one_list[rt][1])

    return dk_list