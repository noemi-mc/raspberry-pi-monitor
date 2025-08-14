from flask import Flask, render_template, jsonify
import sqlite3

app = Flask(__name__)

DB_PATH = "/home/pi/raspberry-pi-monitor/metrics.db"

def get_latest_metrics(limit =50):
	conn = sqlite3.connect(DB_PATH)
	c = conn.cursor()
	c.execute("SELECT timestamp, cpu_percent, memory_percent, disk_percent FROM metrics ORDER BY timestamp DESC LIMIT ?", (limit,))
	rows = c.fetchall()
	conn.close()
	#reverse, oldest first
	return [{"timestamp": r[0], "cpu": r[1], "memory": r[2], "disk": r[3]} for r in reversed(rows)]

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/data")
def data():
	return jsonify(get_latest_metrics())

if __name__ == "__main__":
	app.run(host= "0.0.0.0", port = 5000, debug = True)
