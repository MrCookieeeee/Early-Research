import nltk
from nltk import pos_tag
from nltk.chunk import RegexpParser
from nltk.tokenize import word_tokenize

# 下载NLTK所需的数据
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

# 句子
sentence = "Amy will kill sam."

# 分词
words = word_tokenize(sentence)

# 词性标注
pos_tags = pos_tag(words)

# 定义语法规则，用于匹配主语和谓语
grammar = r"""
    NP: {<DT|JJ|NN.*>+}    # 匹配名词短语
    VP: {<VB.*><NP|PP>*}    # 匹配动词短语
"""

chunk_parser = RegexpParser(grammar)
tree = chunk_parser.parse(pos_tags)

# 打印解析树
print(tree)

# 提取主语、谓语和宾语
subject = ""
verb = ""
object_ = ""

for subtree in tree.subtrees():
    if subtree.label() == 'NP':
        subject = ' '.join([word for word, tag in subtree.leaves()])
    elif subtree.label() == 'VP':
        for word, tag in subtree.leaves():
            if tag.startswith('VB'):
                verb = word
            elif tag in ['NN', 'NNS', 'NNP', 'NNPS']:
                object_ = word

# 打印结果
print("主语:", subject)
print("谓语:", verb)
print("宾语:", object_)
