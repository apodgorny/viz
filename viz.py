import os
import json
import hashlib
import threading
import time
import webbrowser
from typing import Any

import uvicorn
import pandas as pd

from viz_frame  import VizFrame
from viz_series import VizSeries
from viz_info   import VizInfo


class Viz:
	Frame          = VizFrame
	Series         = VizSeries
	Info           = VizInfo

	HOST           = '127.0.0.1'
	PORT           = 8000

	VIZ_PATH       = os.path.abspath(os.path.dirname(__file__))
	JSON_PATH      = os.path.join(VIZ_PATH, 'json')
	STATIC_PATH    = os.path.join(VIZ_PATH, 'static')
	TEMPLATES_PATH = os.path.join(VIZ_PATH, 'templates')

	@classmethod
	def save(cls, endpoint_name, frame):
		json_data = frame.to_json()
		md5       = hashlib.md5(json_data.encode()).hexdigest()

		os.makedirs(cls.JSON_PATH, exist_ok=True)

		data_path = os.path.join(cls.JSON_PATH, f'{md5}.json')
		with open(data_path, 'w', encoding='utf-8') as f:
			f.write(json_data)

		url = f'http://{cls.HOST}:{cls.PORT}/{endpoint_name}/{md5}'
		return url
	
	@classmethod
	def run_server(cls):
		uvicorn.run(
			'server:app',
			host      = cls.HOST,
			port      = cls.PORT,
			log_level = 'error'
		)

	@staticmethod
	def render(view, data):
		url    = Viz.save(view, data)
		thread = threading.Thread(target=Viz.run_server, daemon=True)

		thread.start()
		time.sleep(0.8)
		webbrowser.open(url)
		time.sleep(30)        # Auto-stop after N seconds
