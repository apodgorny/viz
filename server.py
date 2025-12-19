from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
import json
from pathlib import Path


app = FastAPI()

app.mount('/static', StaticFiles(directory='viz_server/static'), name='static')
templates = Jinja2Templates(directory='viz_server/templates')


@app.get('/plot/{viz_id}', response_class=HTMLResponse)
def plot(request: Request, viz_id: str):
	path = Path('viz_data') / f'{viz_id}.json'

	data = json.loads(path.read_text())

	return templates.TemplateResponse(
		'plot.html',
		{
			'request' : request,
			'data'    : data
		}
	)
