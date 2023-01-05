from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
with app.app_context():
    db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Item %r>' % self.id


@app.route('/about/')
def about():
    return render_template('about.html')


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        item_content = request.form['content']
        new_item = Todo(content=item_content)

        try:
            db.session.add(new_item)
            db.session.commit()
            return redirect('/')

        except:
            return 'There was an issue adding to list'

    else:
        items = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', items=items)


@app.route('/delete/<int:id>')
def delete(id):
    item_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting item from list'


@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    item = Todo.query.get_or_404(id)

    if request.method == 'POST':
        item.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your item'
    else:
        return render_template('update.html', item=item)


if __name__ == "__main__":
    app.run(host="localhost", port=8000, debug=True)
