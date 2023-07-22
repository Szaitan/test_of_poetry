from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_bootstrap import Bootstrap
from forms import ContactMeMessage
from flask_ckeditor import CKEditor
from bs4 import BeautifulSoup
import smtplib
import os
from email.mime.text import MIMEText

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("flask_app")
Bootstrap(app)
ckeditor = CKEditor(app)


@app.route("/", methods=["GET"])
def cover_page():
    return render_template("cover.html")


@app.route("/about-me", methods=["GET"])
def about_me_page():
    return render_template("about-me.html")


@app.route("/contact-me", methods=["GET", "POST"])
def contact_me_page():
    form = ContactMeMessage()
    if form.validate_on_submit():
        with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=os.environ.get("my_mail"), password=os.environ.get("my_acc_pass"))

            message_to_send = form.message.data
            name_to_send = form.name.data
            subject = form.subject.data

            list_to_soup = [name_to_send, subject]
            list_to_send = []

            for item in list_to_soup:
                soup = BeautifulSoup(item, 'html.parser')
                text = soup.get_text()
                list_to_send.append(text)

            soup = BeautifulSoup(message_to_send, 'html.parser')
            message_text = soup.get_text()

            msg = MIMEText(f"Subject:{form.subject.data}\n\n{list_to_soup[0]}\n{form.e_mail.data}\n{form.phone_number.data}\n{message_text}", 'plain', 'utf-8')
            msg['Subject'] = list_to_soup[1]

            connection.sendmail(from_addr=os.environ.get("my_mail"), to_addrs=os.environ.get("my_mail"),
                                msg=msg.as_string())
        flash('Your message has been sent. Thank you!', 'success')
        return redirect(url_for('contact_me_page'))
    return render_template("contact.html", form=form)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
