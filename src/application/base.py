from pyltp import Segmentor
import os
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