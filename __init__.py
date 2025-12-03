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


from flask import Flask, jsonify, render_template
import requests
from datetime import datetime
from collections import Counter

app = Flask(__name__)

@app.route('/commits-data/')
def commits_data():
    url = "https://api.github.com/repos/SaraLyna/Projet_metriques_5MCSI_Sara/commits?per_page=30"
    headers = {"User-Agent": "Metriques-App"}  # Obligatoire pour GitHub

    try:
        response = requests.get(url, headers=headers, timeout=10)
    except Exception as e:
        return jsonify({"error": "Request failed", "details": str(e)}), 500

    if response.status_code != 200:
        return jsonify({"error": "GitHub API error", "status": response.status_code, "text": response.text}), 500

    commits = response.json()
    if not isinstance(commits, list):
        return jsonify({"error": "Unexpected API response", "data": commits}), 500

    minutes_list = []
    for commit in commits:
        try:
            author = commit.get("commit", {}).get("author")
            if author and "date" in author:
                date_obj = datetime.strptime(author["date"], '%Y-%m-%dT%H:%M:%SZ')
                minutes_list.append(date_obj.minute)
        except Exception as e:
            print("Commit ignored:", e)
            continue

    if not minutes_list:
        return jsonify({"error": "No valid commit dates found"}), 500

    minute_counts = Counter(minutes_list)
    results = [{"minute": m, "count": c} for m, c in sorted(minute_counts.items())]

    return jsonify({"results": results})

# Page HTML pour afficher l’histogramme
@app.route('/commits/')
def commits_page():
    return render_template('commits.html')


  
if __name__ == "__main__":
  app.run(debug=True)
