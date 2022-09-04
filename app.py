from flask import Flask, render_template, request, redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reviews.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///shop.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
shop_db = SQLAlchemy(app)
reviews_db = SQLAlchemy(app)


class Shop(shop_db.Model):
    id = shop_db.Column(shop_db.Integer, primary_key=True)
    title = shop_db.Column(shop_db.Text, nullable=False)
    price = shop_db.Column(shop_db.Integer, nullable=False)
    isActive = shop_db.Column(shop_db.Boolean, default=True)

    def __repr__(self):
        return self.title


class Reviews(reviews_db.Model):
    id = reviews_db.Column(reviews_db.Integer, primary_key=True)
    text = reviews_db.Column(reviews_db.Text, nullable=False)
    date = reviews_db.Column(reviews_db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Reviews %r>' % self.id


@app.route('/')
def index():
    items = Shop.query.all()
    return render_template('index.html', data=items)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/create', methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        title = request.form['title']
        price = request.form['price']
        all = Shop(title=title, price=price)
        try:
            shop_db.session.add(all)
            shop_db.session.commit()
            return redirect('/')
        except:
            return 'Ошибка'
    else:
        return render_template('create.html')


@app.route('/reviews')
def review():
    reviews = Reviews.query.order_by(Reviews.date).all()
    return render_template('reviews.html', all=reviews)


@app.route('/leave_feedback', methods=['POST', 'GET'])
def leave_feedback():
    if request.method == 'POST':
        text = request.form['text']
        lf = Reviews(text=text)
        try:
            reviews_db.session.add(lf)
            reviews_db.session.commit()
            return redirect('/reviews')
        except:
            return 'При добалении статьи произошла ошибка'
    else:
        return render_template('leave_feedback.html')


if __name__ == '__main__':
    app.run(debug=True)
