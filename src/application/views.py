

from flask import render_template, request, g
from src import app
from src.application.database import db_session, Word_sheet, Speech_sheet, Speaker_sheet
from src.application.base import LtpProcess

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
        session = db_session()

        # 对每一个分词逐一进行循环查询，找出出现所有分词的文章
        i = 0
        query_row_list = []
        for word_str in word_list:
            if i == 0:
                #找出存在第一个分词的文章
                query_row = session.query(Word_sheet.speech_id_of_word).filter_by(word_content=word_str)\
                                   .group_by(Word_sheet.speech_id_of_word).all()
                print(type(query_row))
                print(query_row)
                wd = query_row[0]
                print('*******')
                print(wd)
                print(wd.speech_id_of_word)
                print(query_row_list)

            else:
                #在存在第一个分词的文章中，继续找出是否也存在第二个、第三个.....分词
                query_row = session.query(Word_sheet.speech_id_of_word)\
                    .filter(Word_sheet.speech_id_of_word.in_(query_row_list), Word_sheet.word_content==word_str) \
                    .group_by(Word_sheet.speech_id_of_word).all()
            #把二维列表转化为一维列表
            query_row_list = []
            for query_row_str in query_row:
                query_row_list.append(query_row_str.speech_id_of_word)

            i = i + 1
        # 列出出现所有分词的文章
        query_row_result = session.query(Speech_sheet.speech_id, Speaker_sheet.speaker_name, Speech_sheet.speech_title).join(Speaker_sheet) \
            .filter(Speech_sheet.speech_id.in_(query_row_list)).all()

        db_session.remove()

        return render_template('query_result_wb.html', query_outcome=query_row_result)


@app.route('/b/<int:url_speech_id>', methods=['GET'])
def content_cm(url_speech_id):
    session = db_session()
    sp_content = session.query(Speech_sheet.speech_title, Speech_sheet.speech_content).filter(Speech_sheet.speech_id==url_speech_id).all()
    title_content = sp_content[0][0]
    sp_content = sp_content[0][1]
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