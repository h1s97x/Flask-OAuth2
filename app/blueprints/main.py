from flask import render_template, flash, redirect, url_for, Blueprint

from app.forms import MessageForm
from app.models import Message
from app.extensions import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    form = MessageForm()
    if form.validate_on_submit():
        name = form.name.data
        body = form.body.data
        message = Message(body=body, name=name)
        db.session.add(message)
        db.session.commit()
        flash('Your message have been sent to the world!')
        return redirect(url_for('main.index'))

    messages = Message.query.order_by(Message.timestamp.desc()).all()
    print(form)
    return render_template('main/index.html', form=form, messages=messages)


@main_bp.route('/about')
def about():
    return render_template('main/about.html')
