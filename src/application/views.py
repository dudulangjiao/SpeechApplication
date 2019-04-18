

from flask import render_template, request, session
from src import app
from src.application.database import db_session, Word_sheet, Speech_sheet, Speaker_sheet, Sentence_sheet
from src.application.base import LtpProcess, StringSortWeight, ListGroupBy
from operator import itemgetter
from sqlalchemy import func

"""
# 使用Flask静态文件的时候，每次更新，发现CSS或是Js或者其他的文件不会更新。这是因为浏览器的缓存问题。
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'application/static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                     endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)
"""

@app.route('/')
def index():

    return render_template('index.html')

@app.route('/a', methods=['POST'])
def submit_cm():
    key_words = request.values['get_key_words']

    # 删除关键词前后的空字符
    area_unicode = key_words.strip()

    if not key_words:
        return render_template('index.html', prompt='关键词不能为空，请重新输入：')
    else:
        # 对关键词用类LtpProcess进行分词处理
        ltp_instance = LtpProcess(area_unicode)
        word_list = ltp_instance.ltp_word()  # word_list类型是列表
        sql_session = db_session()

        #找出存在分词的文章
        query_speech_id = sql_session.query(Word_sheet.speech_id_of_word, Word_sheet.index_sentence_of_word_in_speech,
            func.group_concat(Word_sheet.word_content, ''))\
            .group_by(Word_sheet.speech_id_of_word, Word_sheet.index_sentence_of_word_in_speech)\
            .filter(Word_sheet.word_content.in_(word_list)) \
            .all()

        #把词组连接成句子
        list_group_by_instance = ListGroupBy(query_speech_id, [0, 1], 2)
        sen_list = list_group_by_instance.target()

        # 取出每一个句子，赋予排序权重
        tmp_sentence_list = []
        sen_number = 0
        for tmp_sentence in sen_list:
            # 创建StringSortWeight类的实例，对给定的句子，根据词组组合在句子中出现的次数，给与排序所依据的权重
            sort_weight_instance = StringSortWeight(word_list, tmp_sentence[2])
            search_sort_weight = sort_weight_instance.weight()
            tmp_sentence_list.append([])
            # [[关键字权重，讲稿ID]，[......].......]
            tmp_sentence_list[sen_number].extend(tmp_sentence)
            tmp_sentence_list[sen_number].append(search_sort_weight)
            sen_number = sen_number + 1

        print(tmp_sentence_list)
        # 调用ListGroupBy类对句子的权重按文章ID进行分组小计，得出每篇文章的权重
        list_group_by_instance = ListGroupBy(tmp_sentence_list, [0], 1)
        re_list = list_group_by_instance.target()
        print(re_list)

        tmp_sen_id_list = []
        for tmp_sen_id in re_list:
            tmp_sen_id_list.append(tmp_sen_id[0])

        query_speech_title = sql_session.query(Speech_sheet.speech_id, Speaker_sheet.speaker_name,
                                               Speech_sheet.speech_title).join(Speaker_sheet) \
            .filter(Speech_sheet.speech_id.in_(tmp_sen_id_list)).order_by(Speech_sheet.speech_id).all()

        hxd = 0
        for de in query_speech_title:
            re_list[hxd].extend(de)
            hxd = hxd + 1

        re_list.sort(key=itemgetter(1), reverse = True)  # 按权重降序排序

        db_session.remove()

        # word_list列表中的关键字赋值给flask的session，以便进行红色显示
        long = len(word_list)
        session['word_number'] = long  # 关键字数量赋值给flask的session
        for i in range(long):
            i_str = str(i)
            session[i_str] = word_list[i]

        return render_template('query_result_wb.html', query_outcome=re_list)

# 按文稿id查询并展示文稿内容
@app.route('/b/<int:url_speech_id>', methods=['GET'])
def content_cm(url_speech_id):
    sql_session = db_session()
    sp_content = sql_session.query(Speech_sheet.speech_title, Speech_sheet.speech_content)\
        .filter(Speech_sheet.speech_id==url_speech_id).all()
    title_content = sp_content[0][0]
    sp_content = sp_content[0][1]
    sp_content = sp_content.replace('\n', '<br>&nbsp;&nbsp;&nbsp;&nbsp;')  # 把换行符\n转为网页换行符<br>
    # 在多个关键字都插入html代码，变成红色显示
    word_number = session.get('word_number')
    for w_n in range(word_number):
        w_n_str = str(w_n)
        sp_content = sp_content.replace(session.get(w_n_str), '<span style="color:red;">'+ session.get(w_n_str) +'</span>')

    return render_template('speech_context.html', content_title = title_content, content_state=sp_content)

"""
@app.route('/b', methods=['GET'])
def get_post():
    get_theme_original = request.values['get_theme_id']
    cnx = mysql.connector.connect(host='localhost', user='root', password='314159', database='FishFamily')
    cursor = cnx.cursor(dictionary=True)
    query_title = ("SELECT post_title FROM theme_sheet WHERE theme_id={0}").format(get_theme_original)
    cursor.execute(query_title)
    outcome_title = cursor.fetchall()
    query = (
        "SELECT floor_no, louzhu_name, post_time, post_context FROM post_sheet WHERE be_theme_id={0}").format(get_theme_original)
    cursor.execute(query)
    outcome = cursor.fetchall()
    query_row = cursor.rowcount
    cursor.close()
    cnx.close()
    return render_template('moment_result_wb.html', query_title_wb=outcome_title, query_outcome=outcome, query_state=query_row)
"""