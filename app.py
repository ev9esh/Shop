from flask import Flask, render_template, request, redirect
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
# from sqlalchemy import create_engine, MetaData, Table, Integer, String, Column, DateTime, ForeignKey, Numeric
# from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reviews.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
reviews_db = SQLAlchemy(app)
# reviews_db = declarative_base()


# class Reviews(reviews_db):
#     __tablename__ = 'reviews'
#     id = Column(Integer, primary_key=True)
#     text = Column(String, nullable=False)
#     date = Column(DateTime, default=datetime.utcnow)


class Reviews(reviews_db.Model):
    id = reviews_db.Column(reviews_db.Integer, primary_key=True)
    text = reviews_db.Column(reviews_db.Text, nullable=False)
    date = reviews_db.Column(reviews_db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Reviews %r' % self.id


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/reviews')
def review():
    reviews = Reviews.query.order_by(Reviews.date.desc()).all()
    return render_template('reviews.html', rewiews=reviews)


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
