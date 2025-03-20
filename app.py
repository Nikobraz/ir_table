from flask_bootstrap import Bootstrap
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select
from iracingdataapi.client import irDataClient
import re

import settings

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = ("postgresql://" + settings.DB_USER + ":"
                                         + settings.DB_PASS + "@"
                                         + settings.DB_HOST
                                         + ":" + settings.DB_PORT + "/postgres")

db = SQLAlchemy(app)
with app.app_context():
    db.create_all()

class Racer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ir_id = db.Column(db.Integer, unique=True, nullable=False)


def parse_drivers_db():
    with app.app_context():
        members = db.session.execute(select(Racer.id, Racer.ir_id)).all()
    return members


def get_data():
    category_list = ['Oval', 'SportCar','Formula','DirtOval','DirtRoad']
    idc = irDataClient(username=settings.USERNAME, password=settings.PASSWORD)
    drivers = parse_drivers_db()
    listdata = []
    for driver in drivers:
        data = {}
        driver_name = driver[0]
        driver_id = driver[1]
        driver_data = []
        if  4 < len(str(driver_id)) < 9 and re.match(r'\d+', str(driver_id)):
            pass
        else:
            print('Not valid driver id')
            continue
        try:
            driver_data = idc.member(cust_id=driver_id, include_licenses=True)
        except Exception as e:
            print(e)
            print(f"Error with {driver_name} and {driver_id}")
        data['name'] = driver_data["members"][0]["display_name"]
        data['id'] = driver_data["members"][0]["cust_id"]

        for category in category_list:
            data[category + 'SR'] = driver_data['members'][0]['licenses'][category_list.index(category)]['safety_rating']
            data[category + 'License'] = driver_data['members'][0]['licenses'][category_list.index(category)]['group_name']
            try:
                data[category + 'iR'] = driver_data['members'][0]['licenses'][category_list.index(category)]['irating']
            except:
                data[category + 'iR'] = 'No data'
        listdata.append(data)
    return listdata


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        ir_id = request.form.get('id')
        db.session.add(Racer(ir_id=ir_id))
        try:
            db.session.commit()
        except Exception as e:
            print(e)
    with app.app_context():
        db.create_all()
    context = {
        "drivers": get_data()
    }
    return render_template('base.html', **context)


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
