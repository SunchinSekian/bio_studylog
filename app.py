from flask import Flask, render_template, redirect, request
import sqlite3
app = Flask(__name__)
DATABASE = 'data.db'


@app.route("/")
def hello_world():
    try:
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute("select * from entry ")
        data = cur.fetchall()[::-1]
    finally:
        cur.close()
        conn.close()
    return render_template('index.html', data=data)


@app.route('/write', methods=["GET", "POST"])
def write():
    if request.method == 'POST':
        topic = request.form.get('topic')
        main = request.form.get('main')
        tag = request.form.get('tag')
        print(tag)
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute('select * from tag where name=\'%s\'' % tag)
        t = cur.fetchall()
        try:
            conn = sqlite3.connect(DATABASE)
            cur = conn.cursor()
            if t == [] and tag != None:
                cur.execute('insert into tag values(null,?)', (tag,))
            cur.execute("INSERT INTO entry values(null,?,?,?)",
                        (topic, main, tag))
            conn.commit()
        finally:
            cur.close()
            conn.close()
        return redirect('/')
    else:
        return render_template('write.html')


@app.route('/detail/<uid>')
def detail(uid):
    try:
        conn = sqlite3.connect(DATABASE)
        cur = conn.cursor()
        cur.execute("select * from entry where id=%s" % uid)
        data = cur.fetchall()[0]
    finally:
        cur.close()
        conn.close()
    return render_template('detail.html', data=data)


@app.route('/surprise')
def surprise():
    return render_template('test.html')


@app.route('/tags')
def tag():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('select * from tag')
    data = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('tags.html', data=data)
@app.route('/tags/<name>')
def tdetail(name):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute(f'select * from entry where tag={name}')
    data = cur.fetchall()
    cur.close()
    conn.close()
    return str(data)
@app.route('/api')
def api():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('SELECT * FROM entry ORDER BY RANDOM() limit 1')
    data = cur.fetchall()
    cur.close()
    conn.close()
    return str(data)
    
if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
