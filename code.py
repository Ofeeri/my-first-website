from flask import Flask, render_template, url_for, request
import requests
import os

nasa_api = os.environ.get('nasa_api')
link = f'https://api.nasa.gov/planetary/apod?api_key={nasa_api}'

app = Flask(__name__)


def calculate_weights(earth_mass):
	surface_gravities = {'mercury': 0.38, 'venus': 0.91, 'mars': 0.38, 'jupiter': 2.34, 'saturn': 0.93, 'uranus': 0.92, 'neptune': 1.12}
	planet_weights = dict()
	for ele in surface_gravities:
		sg = surface_gravities[ele]
		w = earth_mass * sg
		planet_weights[ele] = round(w, 1)
	return planet_weights


@app.route("/", methods=["POST", "GET"])
def home():
	if request.method == "POST":
		weight = request.form["weight"]
	resp = requests.get(link)
	resp_json = resp.json()
	image = resp_json['url']
	title = resp_json['title']
	return render_template("index.html", image_url=image, title=title)


@app.route("/results", methods=["POST", "GET"])
def results():
	planet_weights = calculate_weights(earth_mass=int(request.form["weight"]))
	return render_template("results.html", planet_weights = calculate_weights(earth_mass=int(request.form["weight"])))


if __name__ == "__main__":
	app.run()