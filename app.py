from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///notes.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'to do' + str(self.id)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/notes',methods=['GET','POST'])
def notes():

    if request.method == 'POST':
        new_title = request.form['title']
        new_content = request.form['content']
        new_note = Todo(title=new_title,content=new_content)
        db.session.add(new_note)
        db.session.commit()
        return redirect('/notes')
    else:
        all_note = Todo.query.all()
        return render_template('notes.html',notes=all_note)

@app.route('/notes/delete/<int:id>')
def delete(id):
    note = Todo.query.get_or_404(id)
    db.session.delete(note)
    db.session.commit()
    return redirect('/notes')

@app.route('/notes/update/<int:id>',methods=['GET','POST'])
def update(id):
    note = Todo.query.get_or_404(id)

    if request.method == 'POST':

        note.title = request.form['title']
        note.content = request.form['content']
        db.session.commit()
        return redirect('/notes')
    else:
        return render_template('update.html', note=note)




if __name__=='__main__':
    app.run(debug=True)