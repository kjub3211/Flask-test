from flask import Flask, render_template, request, redirect, url_for
import re
import random
import string
import os

app = Flask(__name__)

def generate_password(length=12):
    if length < 8:
        length = 8

    upper = random.choice(string.ascii_uppercase)
    lower = random.choice(string.ascii_lowercase)
    digit = random.choice(string.digits)
    special = random.choice("!@#$%^&*()_+-=[]{}|;:,.<>?")

    remaining = length - 4
    all_chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
    others = [random.choice(all_chars) for _ in range(remaining)]

    password_list = list(upper + lower + digit + special + ''.join(others))
    random.shuffle(password_list)

    return ''.join(password_list)


def password_strength(password):
    length_ok = len(password) >= 8
    has_upper = bool(re.search(r'[A-Z]', password))
    has_lower = bool(re.search(r'[a-z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_special = bool(re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>/?\\|`~]', password))

    score = sum([length_ok, has_upper, has_lower, has_digit, has_special])
    secure = score == 5

    return {
        'password_len': len(password),
        'length_ok': length_ok,
        'has_upper': has_upper,
        'has_lower': has_lower,
        'has_digit': has_digit,
        'has_special': has_special,
        'secure': secure,
        'password': password
    }

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        password = request.form['password']
        return redirect(url_for('raport', password=password))
    return render_template('index.html')

@app.route('/generate')
def generate():
    password = generate_password()
    return redirect(url_for('raport', password=password))

@app.route('/raport')
def raport():
    password = request.args.get('password', '')
    result = password_strength(password)
    return render_template('raport.html', **result)

if __name__ == '__main__':
        port = int(os.environ.get("PORT", 5000))
        app.run(host="0.0.0.0", port=port, debug=True)

