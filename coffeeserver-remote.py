from flask import Flask
from flask import render_template, request, send_from_directory
from flask import jsonify
import time
import sched
import urllib.request
import threading
import _mysql
import os

app = Flask(__name__, static_url_path='')

@app.route("/scripts/<path:path>")
def return_script(path):
	print("returning script file")
	return send_from_directory('scripts', path)

@app.route("/coffee")
def make_coffee_pagesql():
	return render_template('/templatesql.tpl')


@app.route("/coffee/datasql/")
def send_coffee_data_jsonsql():
	print("making mysql page")
	points = []
	uname = str(os.getenv('SQLUNAME'))
	pwd = str(os.getenv('SQLPWD'))
	host = str(os.getenv('SQLHOST'))
	port = int(os.getenv('SQLPORT'))
	print(uname)
	print(pwd)
	print(host)
	print(port)
	db = _mysql.connect(
	    user=uname, passwd=pwd,
	    host=host, port=port,
	    db=uname,
	)	
	db.query("SELECT * FROM Weights")
	r=db.store_result()
	for rw in r.fetch_row(maxrows=0):
		points.append([1000 * int(rw[0]), -1 * float(rw[1])])
	output = {"data": points}
	return jsonify(output)	

if __name__ == "__main__":
	port = int(os.environ.get("PORT", 5000))
	app.run(host='0.0.0.0', port=port)

