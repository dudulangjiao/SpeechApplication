

from flask import render_template, request, session
from src import app
from src.application.database import db_session, Word_sheet, Speech_sheet, Speaker_sheet, Sentence_sheet
from src.application.base import LtpProcess, StringSortWeight
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

        # 对每一个分词逐一进行循环查询，找出出现所有分词的文章
        i = 0
        tmp_word_list = []  # 用来临时保存查询的讲稿ID列表

        for word_str in word_list:
            if i == 0:
                #找出存在第一个分词的文章
                query_speech_id = sql_session.query(Word_sheet.speech_id_of_word).filter_by(word_content=word_str)\
                                   .group_by(Word_sheet.speech_id_of_word).all()

            else:
                #在存在第一个分词的文章中，继续找出也同时存在第二个、第三个.....分词的文章
                query_speech_id = sql_session.query(Word_sheet.speech_id_of_word)\
                    .filter(Word_sheet.speech_id_of_word.in_(tmp_word_list), Word_sheet.word_content==word_str) \
                    .group_by(Word_sheet.speech_id_of_word).all()

            #把查询到的讲稿ID结果，格式从二维列表转化为一维列表，暂时保存到tmp_word_list
            tmp_word_list = []
            for speech_id_str in query_speech_id:
                tmp_word_list.append(speech_id_str.speech_id_of_word)

            i = i + 1

        # 列出出现所有分词的文章
        query_row_result = sql_session.query(Speech_sheet.speech_id, Speaker_sheet.speaker_name, Speech_sheet.speech_title).join(Speaker_sheet) \
            .filter(Speech_sheet.speech_id.in_(tmp_word_list)).all()

        # 根据词组组合在文章中出现的次数，对文章进行排序
        # 列出一个句子中同时出现两个及以上关键词的句子(含相同的重复关键词)
        query_sen_result = sql_session.query(Word_sheet.speech_id_of_word, Word_sheet.index_sentence_of_word_in_speech, func.count('*')) \
                    .filter(Word_sheet.speech_id_of_word.in_(tmp_word_list), Word_sheet.word_content.in_(word_list)) \
                    .group_by(Word_sheet.speech_id_of_word, Word_sheet.index_sentence_of_word_in_speech).having(func.count('*')>1).all()
        #print('列出一个句子中同时出现两个及以上关键词的句子(含相同的重复关键词)')
        #print(query_sen_result)


        # 取出每一个句子，赋予排序权重
        tmp_sentence_list = [[] for i in range(len(query_sen_result))]

        sen_number = 0
        for query_sen_result_list in query_sen_result:
            tmp_query_sentence = sql_session.query(Sentence_sheet.speech_id_of_sentence,
                                                   Sentence_sheet.index_sentence_in_speech,
                                                   Sentence_sheet.sentence_content) \
                    .filter(Sentence_sheet.speech_id_of_sentence == query_sen_result_list.speech_id_of_word,
                            Sentence_sheet.index_sentence_in_speech == query_sen_result_list.index_sentence_of_word_in_speech) \
                    .all()
            #print('*********************************************')
            #print(tmp_query_sentence)
            for tmp__query_sen_list in tmp_query_sentence:
                tmp_sentence = tmp__query_sen_list.sentence_content


            # 创建StringSortWeight类的实例，对给定的句子，根据词组组合在句子中出现的次数，给与排序所依据的权重,并累加成文章排序的权重
            sort_weight_instance = StringSortWeight(word_list, tmp_sentence)
            search_sort_weight = sort_weight_instance.weight()

            tmp_sentence_list[sen_number].append(search_sort_weight)
            tmp_sentence_list[sen_number].append(query_sen_result_list.speech_id_of_word)
            tmp_sentence_list[sen_number].append(query_sen_result_list.index_sentence_of_word_in_speech)
            tmp_sentence_list[sen_number].append(tmp_sentence)
            sen_number = sen_number + 1

        tmp_sentence_list.sort(key=lambda s: s[0], reverse=False)
        print(tmp_sentence_list)


        db_session.remove()

        # word_list列表中的关键字赋值给flask的session
        long = len(word_list)
        session['word_number'] = long  # 关键字数量赋值给flask的session
        for i in range(long):
            i_str = str(i)
            session[i_str] = word_list[i]

        return render_template('query_result_wb.html', query_outcome=query_row_result)

# 按文稿id查询并展示文稿内容
@app.route('/b/<int:url_speech_id>', methods=['GET'])
def content_cm(url_speech_id):
    sql_session = db_session()
    sp_content = sql_session.query(Speech_sheet.speech_title, Speech_sheet.speech_content).filter(Speech_sheet.speech_id==url_speech_id).all()
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