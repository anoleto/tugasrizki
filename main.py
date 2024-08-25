from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import re

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('articles.db')
    conn.execute('''create table if not exists articles
                    (id integer primary key autoincrement,
                     title text unique not null,
                     content text not null,
                     image text,
                     category text);''') # ?
    conn.close()

def parse_content(content):
    parsed_content = re.sub(r'\[img\](.*?)\[/img\]', r'<img src="\1" alt="Image" style="max-width:100%; height:auto;">', content) # lol!
    return parsed_content

@app.route('/')
def index():
    conn = sqlite3.connect('articles.db')
    cursor = conn.execute("select id, title from articles")
    articles = cursor.fetchall()
    conn.close()
    return render_template('index.html', articles=articles)

@app.route('/page/<int:id>')
def page(id):
    conn = sqlite3.connect('articles.db')
    cursor = conn.execute(f"select title, content, image from articles where id={id}")
    article = cursor.fetchone()
    conn.close()

    if article is None:
        return redirect(url_for('index'))

    parsed_content = parse_content(article[1])

    return render_template('page.html', article=(article[0], parsed_content))

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        conn = sqlite3.connect('articles.db')
        conn.execute(f"insert into articles (title, content) values ({title}, {content})")
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('create.html')

if __name__ == '__main__':
    init_db()
    app.run(port=1312, debug=True)