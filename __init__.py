from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
    return render_template('hello.html')


@app.route("/contact/")
def MaPremiereAPI():
    return render_template('contact.html')


@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)

@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def monhistogramme():
    return render_template('histogramme.html')


@app.route('/extract-minutes/<date_string>')
def extract_minutes(date_string):
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    minutes = date_object.minute
    return jsonify({'minutes': minutes})

GITHUB_API_URL = "https://api.github.com/repos/SaraLyna/Projet_metriques_5MCSI_Sara/commits"

@app.route('/commits-data/')
def get_commits_data():
    # Récupérer les données depuis l'API GitHub
    response = urlopen(GITHUB_API_URL)
    raw_content = response.read()
    commits = json.loads(raw_content.decode('utf-8'))
    
    # Initialiser un dictionnaire pour compter les commits par minute
    minutes_count = {i: 0 for i in range(60)}
    
    # Extraire les minutes de chaque commit et compter
    for commit in commits:
        date_string = commit['commit']['author']['date']
        date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
        minute = date_object.minute
        minutes_count[minute] += 1
    
    return jsonify(minutes_count)



@app.route('/commits/')
def commits_page():
    return render_template('commits.html')


  
if __name__ == "__main__":
  app.run(debug=True)
