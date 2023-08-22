import os
import requests 
import xml.etree.ElementTree as ET
import pymysql
from flask import Flask, request, render_template

app = Flask(__name__)

# 获取环境变量
host = os.environ.get('MYSQL_HOST')
user = os.environ.get('MYSQL_USERNAME') 
passwd = os.environ.get('MYSQL_PASSWORD')
db = os.environ.get('MYSQL_NAME')
port = os.environ.get('MYSQL_PORT')
# 连接数据库
db = pymysql.connect(host=host, user=user, passwd=passwd, db=db, port=port)
cursor = db.cursor() 


@app.route('/', methods=['GET', 'POST'])  
def index():
  if request.method == 'POST':
    text = request.form['text']
    id = request.form['id']
    url = f'http://api.microsofttranslator.com/v2/Http.svc/Translate?appId=AFC76A66CF4F434ED080D245C30CF1E71C22959C&from=&to=zh&text={text}'
    response = requests.get(url)
    result = response.text
    root = ET.fromstring(result)

    translated_text = root.find('string').text
    
    # 保存到数据库
    insert_sql = "INSERT INTO translations (id, english, chinese) VALUES (%s, %s, %s)"
    cursor.execute(insert_sql, (id, text, translated_text)) 
    db.commit()

  return render_template('index.html')

if __name__ == '__main__':
    app.run()
