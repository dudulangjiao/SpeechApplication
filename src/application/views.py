from flask import render_template, request
from src import app

@app.route('/')
def index():
    return '欢迎'

    """
    return render_template('index.html')

@app.route('/a', methods=['POST'])
def submit_cm():
    key_words = request.values['get_key_words']

    # 防止地区名称前后有空字符
    area_unicode = key_words.strip()

    if not key_words:
        return render_template('index.html', prompt='关键词不能为空，请重新输入：')
    else:
        cnx = mysql.connector.connect(host=app.config['DB_HOST'], user='root', password='314159', database='FishFamily')
        cursor = cnx.cursor(dictionary=True)
        query = ("SELECT theme_sheet.theme_id, theme_sheet.post_title, post_sheet.area, post_sheet.post_id FROM theme_sheet, post_sheet WHERE theme_sheet.theme_id=post_sheet.be_theme_id AND post_sheet.area='{0}' AND post_sheet.floor_no=1").format(area_unicode)
        cursor.execute(query)
        outcome = cursor.fetchall()
        query_row = cursor.rowcount
        cursor.close()
        cnx.close()
        return render_template('query_result_wb.html', query_outcome=outcome, query_state=query_row)

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