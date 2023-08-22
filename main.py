import os
from flask import Flask, render_template, request
import pymysql
from google.cloud import translate

app = Flask(__name__)

# 获取环境变量
host = os.environ.get('DB_HOST')
user = os.environ.get('DB_USER') 
passwd = os.environ.get('DB_PASSWD')
db = os.environ.get('DB_NAME')
port = os.environ.get('DB_PORT')
# 连接数据库
db = pymysql.connect(host=host, user=user, passwd=passwd, db=db, port=port)
cursor = db.cursor() 

# 创建翻译客户端
translate_client = translate.Client()

@app.route('/', methods=['GET', 'POST'])
def index():

  if request.method == 'POST':
    english_lines = request.form['english'].split('\n')
      
    id = request.form['id']
    
    for line in english_lines:
      english_word = line.strip()
      if english_word:  
        translation = translate_client.translate(english_word, target_language='zh-CN')
        chinese = translation['translatedText']
        
        cursor.execute("INSERT INTO words (id, english, chinese) VALUES (%s, %s, %s)", (id, english_word, chinese))
        db.commit()

  return render_template('index.html')

if __name__ == '__main__':
  app.run()
