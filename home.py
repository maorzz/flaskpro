from flask import Flask, redirect, url_for, render_template, request, session, flash, redirect
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///table.db'
db = SQLAlchemy(app)


################################################


class Table(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)
    takala_desc = db.Column(db.String(1000))

    def __repr__(self):
        return '<name %r>' % self.id


@app.route("/table", methods=["GET", "POST"])
def table():
    if request.method == "POST":

        event_name = request.form['event']
        new_event = Table(name=event_name)

        try:
            db.session.add(new_event)
            db.session.commit()
            return redirect('/table')
        except:
            return"there was an error creating"

    else:
        events = Table.query.order_by(Table.date_created)
        return render_template("table.html", events=events)


@app.route("/update/<int:id>",  methods=["GET", "POST"])
def update(id):
    table_to_update = Table.query.get_or_404(id)
    if request.method == "POST":
        table_to_update.name = request.form['event']
        try:
            db.session.commit()
            return redirect('/table')
        except:
            return "THERE WAS A PROBLEM"
    else:
        return render_template('update.html', table_to_update=table_to_update)


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
