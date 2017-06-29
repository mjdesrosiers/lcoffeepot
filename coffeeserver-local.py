from flask import Flask
from flask import render_template, request, send_from_directory
from flask import jsonify
import time
import sched
import urllib.request
import threading
import _mysql

def retrieve_coffee_data(filename, t_naught=None):
	print('\t[rcd] [getting coffee data]')
	if not t_naught:
		t_naught = int(time.time())
	try:		
		tnow = int(time.time());		
		resp = urllib.request.urlopen('http://192.168.4.1/' + str(tnow), timeout=2);
		html = resp.read().decode('utf-8');

		html = html.split('\n')
		time_start = int(html[2])
		if (time_start != 0):
			data = html[3][:-8]
			data = [float(x) for x in data.split(',')]
			timestamps = [x + time_start - t_naught for x in range(0, len(data))]



			with open(filename, "a") as f:
				for pair in zip(timestamps, data):
					time_to_write = pair[0] + t_naught
					weight_to_write = pair[1]					
					f.write(str(time_to_write) + ", " + str(weight_to_write) + "\n")
					write_to_db(time_to_write, weight_to_write)

			# FULL_TIMESTAMP_DATA.extend(timestamps)
			# FULL_WEIGHT_DATA.extend(data)

			print('\t[rcd] [Added {0} new points]'.format(str(len(data))))			
		else:
			print("\t[rcd] [synchronizing, received zero]")		
	except Exception as e:
		print("\t[rcd] [error: {}]".format(str(e)))
	t = threading.Timer(5.0, retrieve_coffee_data, [filename, t_naught])
	t.daemon = True
	t.start()

def write_to_db(time, weight):
	print("writing to db")
	uname = os.getenv('SQLUNAME')
	pwd = os.getenv('SQLPWD')
	host = os.getenv('SQLHOST')
	port = os.getenv('SQLPORT')
	db = _mysql.connect(
	    user=uname, passwd=pwd,
	    host=port, port=port,
	    db=uname,
	)	
	LN1 = "INSERT INTO Weights (Timestamp, Weight)"
	LN2 = "VALUES ({}, {});".format(time, weight)
	db.query(LN1 + "\n" + LN2);
	r=db.store_result()
	if (r):
	    print(r.fetch_row())	

if __name__ == "__main__":
	retrieve_coffee_data('COFFEELOG.csv')		
	while True:
		time.sleep(10)

