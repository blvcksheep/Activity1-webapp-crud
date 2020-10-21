from flask import (Flask, redirect, render_template, request, url_for, flash)
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "secreto-sa-pato"


# MySQL configurations
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'studentapp'

mysql = MySQL(app)


class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'


user = (User(username='ADMIN', password='password'))


@app.route('/', methods=['GET', 'POST'])
def login_Page():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if user.username == username and user.password == password:
            return redirect(url_for('system'))

        return redirect(url_for('login_Page'))

    return render_template('login.html')


@app.route('/system')
def system():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM students')
    data = cur.fetchall()
    cur.close()
    return render_template('system.html', outputData=data)


@app.route('/addstud', methods=['POST'])
def addStudent():
    cur = mysql.connection.cursor()
    if request.method == 'POST':
        name = request.form['name']
        course = request.form['course']
        yearLevel = request.form['yearLevel']
        email = request.form['email']
        cur.execute("INSERT INTO students (name, course, yearLevel, email) VALUES (%s,%s,%s,%s)",
                    (name, course, yearLevel, email))
        mysql.connection.commit()
        flash('Student Added Successfully')
        return redirect(url_for('system'))


@app.route('/edit/<id>', methods=['POST', 'GET'])
def getStudent(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM students WHERE id = %s', [id])
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit.html', outputData=data, )


@app.route('/update/<id>', methods=['POST'])
def updateStudent(id):
    if request.method == 'POST':
        name = request.form['name']
        course = request.form['course']
        yearLevel = request.form['yearLevel']
        email = request.form['email']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE students
            SET name = %s,
                course = %s,
                yearLevel = %s,
                email = %s
            WHERE id = %s
        """, (name, course, yearLevel, email, id))
        flash('Student Updated Successfully')
        mysql.connection.commit()
        return redirect(url_for('system'))


@app.route('/delete/<string:id>', methods=['POST', 'GET'])
def deleteStudents(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM students WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Student Removed Successfully')
    return redirect(url_for('system'))


if __name__ == "__main__":
    app.run(debug=True)
