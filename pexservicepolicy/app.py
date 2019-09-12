# -*- coding: utf-8 -*-
from flask import flash, redirect, Flask, render_template, request, jsonify, Response
import os
from forms import HelloForm, VmrForm
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import logging
from logging.handlers import RotatingFileHandler
import re
import json
from config import Config


app = Flask(__name__)
app.secret_key = 'dev'
# app.config.from_object(os.environ['APP_SETTINGS'])
app.config.from_object(Config)

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)


# DB Models
class Vmrs(db.Model):    
    id = db.Column(db.Integer, primary_key=True)
    local_alias = db.Column(db.String(80), unique=True, nullable=False)
    name = db.Column(db.String(100), unique=True, nullable=False)
    pin = db.Column(db.Integer, unique=False)
    guest_pin = db.Column(db.Integer, unique=False)
    host_view = db.Column(db.String(100), nullable=False, default='one_main_seven_pips')
    allow_guests = db.Column(db.Boolean, unique=False, default=True)
    guests_can_present = db.Column(db.Boolean, unique=False, default=True)
    is_active = db.Column(db.Boolean, unique=False, default=True)

    # def __init__(self, local_alias, name, pin, guest_pin, host_view, allow_guests, guests_can_present, is_active ):
    #     self.local_alias = local_alias
    #     self.name = name
    #     self.pin = pin
    #     self.guest_pin = guest_pin
    #     self.host_view = host_view
    #     self.allow_guests = allow_guests
    #     self.guests_can_present = guests_can_present
    #     self.is_active = is_active
        
    def __repr__(self):
        return '<Name {}>'.format(self.id)



@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500


'''
curl -X GET 'http://localhost:5000/policy/v1/service/configuration?P-Asserted-Identity="Alice"<sip:alice@example.com>\
&protocol=mssip&node_ip=10.47.2.43&registered=False&remote_address=10.47.2.20&\
version_id=16&bandwidth=0&pseudo_version_id=36402.0.0\
&vendor=UCCAPI/16.0.7967.5277 OC/16.0.7967.2139 (Skype for Business)&\
local_alias=sip:meet.alice@example.com&remote_port=63726&\
call_direction=dial_in&remote_alias=sip:alice@example.com&\
remote_display_name=Alice&trigger=invite&location=London'
'''


    



# Functions

# Policy:
@app.route('/policy/v1/service/configuration', methods=['GET'])
def policy():
    local_alias = re.sub(r"(sip|h323):", "", request.args['local_alias'])
    remote_display_name = request.args['remote_display_name']
    remote_alias = request.args['remote_alias']
    call_direction = request.args['call_direction']

    if call_direction == 'dial_in':
        qry = db.session.query(Vmrs).filter(
                    Vmrs.local_alias==local_alias)
        vmr = qry.first()
        if vmr:    
            app.logger.info('Matched request: {}'.format(dict(request.args)))
            if vmr.pin is None:
                vmr.pin = ''
            if vmr.guest_pin is None:
                vmr.guest_pin = ''
                
            policy_resp = {
"status" : "success",
"result" : {
  "service_type" : "conference",
  "name" : vmr.name,
  "service_tag" : "adhoc",
  "description" : "Adhoc VMR",
  "pin" : str(vmr.pin),
  "guest_pin" : str(vmr.guest_pin),
  "guests_can_present" : vmr.guests_can_present,
  "allow_guests" : vmr.allow_guests,
  "view" : vmr.host_view,
  "automatic_participants" : []
  },
"dennis_version" : "1.0"}

            result = json.dumps(policy_resp)
            app.logger.info('Policy response: {}'.format(result))
            return Response(response=result, status=200, mimetype="application/json")

        else:
            app.logger.info("Didn't match request: {}".format(dict(request.args)))
            return "Did not match"
    return jsonify("ok")

# Web views

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/new_vmr', methods=['GET', 'POST'])
def new_vmr():
    error = None
    """
    Add a new VMR
    """
    form = VmrForm(request.form)

    if request.method == 'POST' and form.validate() and form.validate_on_submit():
        try:
            vmr = Vmrs()
            vmr.name = form.name.data
            vmr.local_alias = form.local_alias.data
            # vmr.pin = form.pin.data
            # vmr.guest_pin = form.guest_pin.data
            if form.pin.data == '':
                vmr.pin = None
            if form.guest_pin.data == '':
                vmr.guest_pin = None   
            vmr.is_active = form.is_active.data
            vmr.host_view = form.host_view.data
            vmr.allow_guests = form.allow_guests.data
            vmr.guests_can_present = form.guests_can_present.data

            db.session.add(vmr)
            db.session.commit()

            flash("Successfully created a new VMR")
            return redirect('./new_vmr')
        except IntegrityError as e:
            db.session.rollback()
            return render_template("500.html", error = str(e))

    return render_template('new_vmr.html', form=form, error=error)



@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    qry = db.session.query(Vmrs).filter(
                Vmrs.id==id)
    vmr = qry.first()
 
    if vmr:
        form = VmrForm(formdata=request.form, obj=vmr)
        if request.method == 'POST' and form.validate() and form.validate_on_submit():
            # save edits
            try:
                vmr.name = form.name.data
                vmr.local_alias = form.local_alias.data
                vmr.pin = form.pin.data
                vmr.guest_pin = form.guest_pin.data
                vmr.is_active = form.is_active.data
                vmr.host_view = form.host_view.data
                vmr.allow_guests = form.allow_guests.data
                vmr.guests_can_present = form.guests_can_present.data
                db.session.commit()

                flash("Successfully created a new VMR")
                return redirect('/vmrs')
            except IntegrityError as e:
                db.session.rollback()
                return render_template("500.html", error = str(e))
        return render_template('edit_vmr.html', form=form)
    else:
        return 'Error loading #{id}'.format(id=id)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    # qry = db.session.query(Vmrs).filter(
    #             Vmrs.id==id)
    vmr = Vmrs.query.filter_by(id=id).one()
    # vmr = qry.first()
    try:
        db.session.delete(vmr)
        db.session.commit()

        flash("Successfully deleted VMR")
        return redirect('/vmrs')
    except IntegrityError as e:
        db.session.rollback()
        return render_template("500.html", error = str(e))
    return redirect('/vmrs')
 
@app.route('/vmrs', methods=['GET', 'POST'])
def vmrs_list():

    page = request.args.get('page', 1, type=int)
    pagination = Vmrs.query.paginate(page, per_page=10)
    vmrs = pagination.items
    return render_template('pagination.html', pagination=pagination, vmrs=vmrs)

if __name__ == '__main__':
    ''' Logging config: '''
    logHandler = RotatingFileHandler('events.log', maxBytes=10000, backupCount=1)

    # set the log handler level
    logHandler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logHandler.setFormatter(formatter)
    # set the app logger level
    app.logger.setLevel(logging.INFO)

    app.logger.addHandler(logHandler)
    app.logger.info('Starting app') 
    app.run(host="0.0.0.0")

