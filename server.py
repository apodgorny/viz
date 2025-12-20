import os
import json

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from viz import Viz


app = FastAPI()

app.mount(
	'/static',
	StaticFiles(directory=Viz.STATIC_PATH),
	name='static'
)

templates = Jinja2Templates(directory=Viz.TEMPLATES_PATH)


@app.get('/plot/{uid}', response_class=HTMLResponse)
def plot(request: Request, uid: str):
	path = os.path.join(Viz.JSON_PATH, f'{uid}.json')

	with open(path, 'r', encoding='utf-8') as f:
		json_data = f.read()

	os.remove(path)

	return templates.TemplateResponse(
		'plot.html',
		{
			'request' : request,
			'data'    : json_data
		}
	)
