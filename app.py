from flask import Flask, render_template, request
import pickle
import requests

app = Flask(__name__)


movies = pickle.load(open('model/movie_list.pkl', 'rb'))
similarity = pickle.load(open('model/similarity.pkl', 'rb'))



def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movie_names, recommended_movie_posters

# @app.route('/', methods=['GET', 'POST'])
# def home():
#     movie_list = movies['title'].values
#     if request.method == 'POST':
#         selected_movie = request.form['movie']
#         names, posters = recommend(selected_movie)
#         return render_template('recommend.html', movies=names, posters=posters)
#     return render_template('index.html', movie_list=movie_list)
# @app.route('/', methods=['GET', 'POST'])
# def home():
#     movie_list = movies['title'].values
#     if request.method == 'POST':
#         selected_movie = request.form['movie']
#         names, posters = recommend(selected_movie)

       
#         zipped_data = zip(names, posters)

  
#         return render_template('recommend.html', data=zipped_data)
    
#     return render_template('index.html', movie_list=movie_list)
@app.route('/', methods=['GET', 'POST'])
def home():
    movie_list = movies['title'].values
    if request.method == 'POST':
        selected_movie = request.form['movie']
        names, posters = recommend(selected_movie)
        zipped_data = zip(names, posters)
        return render_template('index.html', movie_list=movie_list, data=zipped_data)
    
    return render_template('index.html', movie_list=movie_list)

if __name__ == '__main__':
    app.run(debug=True)

