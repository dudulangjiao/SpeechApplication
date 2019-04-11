from pyltp import Segmentor
import os
import re
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

def process_page(page_content):
    """创建一个函数，用来对文本进行删除换行符、空格等处理"""

    remove_n = re.compile('\\n')  # 去除换行符\n
    #remove_square = re.compile('■')  # 去除■
    #remove_space = re.compile(' ')  # 去除空格

    page_content = remove_n.sub('<br>&nbsp;&nbsp;&nbsp;&nbsp;', page_content)
    #page_content = remove_square.sub('', page_content)
    #page_content = remove_space.sub('', page_content)

    return page_content