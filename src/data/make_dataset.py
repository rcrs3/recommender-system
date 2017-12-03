import requests, json, csv, os, pandas

API_URL = "http://www.omdbapi.com/"
API_KEY = "Your Key"

# change these paths for the path you're using
# "~" gonna cover os/user
DATA_PATH = "../../data/raw/movies_list.csv"
MOVIES_NAMES_PATH = "movies_names_list.csv"

# transform the dic values into csv format
def transform_to_csv(dic_vals):
        
    keys = dic_vals.keys()
    
    with open(os.path.expanduser(DATA_PATH), 'a') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writerow(dic_vals)

# transform the csv file containing the list of movies
# into an array
def read_movie_names():
    colnames = ["Title"]
    data = pandas.read_csv(MOVIES_NAMES_PATH, names=colnames)
    movie_names = data["Title"].tolist()
    movie_names.pop(0)
    return movie_names

# do a request for each movie
def do_requests():
    movie_names = read_movie_names()
    for movie_name in movie_names:
        try:
            params = {
                "t": movie_name,
                "apikey": API_KEY,
                "plot": "full",
                "type": "movie"
            }
            response = requests.get(API_URL, params)
            python_dic_values = json.loads(response.text)
            transform_to_csv(python_dic_values)
        except:
            continue
        
do_requests()        
