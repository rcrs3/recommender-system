import json
import requests

from os.path import dirname, join, realpath

OMDB_URL = 'http://www.omdbapi.com/'

dir_name = dirname(realpath(__file__))

with open(join(dir_name, 'api_key.json')) as api_key_json:
	data = json.load(api_key_json)
	OMDB_API_KEY = data['omdb_key']
	
def fetch_movie_info(movie_name):
	params = {
		'apikey': OMDB_API_KEY,
		't': movie_name,
		'type': movie,
		'plot': full
	}
	
	try:
		res = requests.get(OMDB_URL, params = params)
	except:
		raise StopIteration('timeout')
		
	if res.ok:
		data = json.loads(res.content)
		
		return data
		
	else
		raise StopIteration('timeout')
