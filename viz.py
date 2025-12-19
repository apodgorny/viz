import os
import json
import hashlib
import threading
import time
import webbrowser
from typing import Any

import uvicorn
import pandas as pd

from wordwield import ww


DATA_PATH = os.path.join(ww.config.WW_PATH, 'viz', 'json')
HOST      = '127.0.0.1'
PORT      = 8000


class Viz:
	@staticmethod
	def to_json(data: Any):
		json_data = '{}'
		if isinstance(data, pd.DataFrame):
			json_data = data.to_json(orient='records')
		else:
			json_data = json.dumps(data, ensure_ascii=False)
		return json_data

	@staticmethod
	def save(endpoint_name, data):
		json_data = Viz.to_json(data)
		md5       = hashlib.md5(json_data.encode()).hexdigest()

		os.makedirs(DATA_PATH, exist_ok=True)

		data_path = os.path.join(DATA_PATH, f'{md5}.json')
		with open(data_path, 'w', encoding='utf-8') as f:
			f.write(json_data)

		url = f'http://{HOST}:{PORT}/{endpoint_name}/{md5}'
		return url
	
	@staticmethod
	def run_server():
		uvicorn.run(
			'viz_server.server:app',
			host      = HOST,
			port      = PORT,
			log_level = 'error'
		)

	@staticmethod
	def render(endpoint_name, data):
		url    = Viz.save(endpoint_name, data)
		thread = threading.Thread(target=Viz.run_server, daemon=True)

		thread.start()
		time.sleep(0.8)
		webbrowser.open(url)
		time.sleep(30)        # Auto-stop after N seconds
