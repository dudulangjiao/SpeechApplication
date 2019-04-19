from pyltp import Segmentor
import os
from operator import itemgetter

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


class StringSortWeight(object):
    """函数:给定一个词组列表和一个字符串，查找字符串中是否含有词组列表的任何组合，并返回权重.

    Attributes:
                word_list: 词组列表
                str_content： 字符串内容

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
        word_list_number = (len(self.word_list))  #1
        sort_weight = 0  # 权重
        for word_int in range(word_list_number):
            word_long = word_list_number - word_int  # 从最长的词组组合长度word_list_number开始 1
            combination_number = word_int + 1  #  各种组合的可能性数量 1
            # 循环取得给定长度的所有词组组合,以词组组合在字符串中出现的次数，赋予其权重并对权重进行累加，返回最后总权重
            for begin_str in range(combination_number): #1
                tmp_word_str = self.word_join(begin_str, word_long)
                integration = self.str_content.count(tmp_word_str)
                if integration > 0:  # 若词组组合在字符串中出现的次数大于0
                    sort_weight = integration*pow(word_long, word_long) + sort_weight

        return sort_weight


class ListGroupBy(object):
    """创建一个函数，按1个或2个列进行分组合计或字符串连接。"""
    def __init__(self, one_list, group_col_list, target_col_no):
        self.one_list = one_list
        self.group_col_list = group_col_list
        self.target_col_no = target_col_no

    def target(self):
        if len(self.group_col_list) == 1:
            one = self.group_col_list[0]
            target = self.target_col_no
            self.one_list.sort(key=itemgetter(one), reverse = False)  # 按第group_col_no列升序排序

            ll = len(self.one_list)
            # [[关键字权重，讲稿ID]，[......].......]
            dk_list = [[]]
            dk_list[0].append(self.one_list[0][one])
            dk_list[0].append(self.one_list[0][target])
            wwt = 0
            for rt in range(ll):
                if rt == 0:
                    pass
                elif self.one_list[rt][one] == self.one_list[rt-1][one]:
                    dk_list[wwt][1] = dk_list[wwt][1] + self.one_list[rt][target]
                elif self.one_list[rt][one] != self.one_list[rt-1][one]:
                    wwt = wwt + 1
                    dk_list.append([])
                    dk_list[wwt].append(self.one_list[rt][one])
                    dk_list[wwt].append(self.one_list[rt][target])

            return dk_list

        elif len(self.group_col_list) == 2:
            one = self.group_col_list[0]
            two = self.group_col_list[1]
            target = self.target_col_no
            self.one_list.sort(key=itemgetter(one, two), reverse=False)  # 按第group_col_no列升序排序
            ll = len(self.one_list)
            # [[关键字权重，讲稿ID]，[......].......]
            dk_list = [[]]
            dk_list[0].append(self.one_list[0][one])
            dk_list[0].append(self.one_list[0][two])
            dk_list[0].append(self.one_list[0][target])
            wwt = 0

            for rt in range(ll):
                if rt == 0:
                    pass
                elif self.one_list[rt][one] == self.one_list[rt - 1][one] and self.one_list[rt][two] == self.one_list[rt - 1][two]:
                    dk_list[wwt][2] = dk_list[wwt][2] + self.one_list[rt][target]
                elif self.one_list[rt][one] != self.one_list[rt - 1][one] or self.one_list[rt][two] != self.one_list[rt - 1][two]:
                    wwt = wwt + 1
                    dk_list.append([])
                    dk_list[wwt].append(self.one_list[rt][one])
                    dk_list[wwt].append(self.one_list[rt][two])
                    dk_list[wwt].append(self.one_list[rt][target])
            return dk_list