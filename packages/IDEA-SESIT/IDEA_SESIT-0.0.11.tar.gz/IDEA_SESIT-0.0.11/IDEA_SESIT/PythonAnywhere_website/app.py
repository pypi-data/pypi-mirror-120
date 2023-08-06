from flask import Flask, render_template
from flask.wrappers import Request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/copper')
def copper():
    return render_template('copper.html')

@app.route('/buildings')
def buildings():
    return render_template('building.html')

@app.route('/message')
def message():
    return render_template('message.html')

@app.route('/silver')
def silver():
    return render_template('silver.html')

@app.route('/transport')
def transfport():
    return render_template('transport.html')

@app.route('/silver/stacked_plot')
def silver_stacked_plot():
    return render_template('stacked_plot.html')

@app.route('/silver/total_generation_plot')
def silver_total_generation_plot():
    return render_template('total_generation_plot.html')

if __name__ == '__main__':
    app.run()