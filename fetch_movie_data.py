import requests
import pandas as pd
import time

API_KEY = "29b087349d9a69bdf5f3c647ab7aba2c"  # Your API key
BASE_URL = "https://api.themoviedb.org/3"
NUM_PAGES = 500  # Fetch 500 pages (10,000 movies)

def fetch_genre_mapping():
    url = f"{BASE_URL}/genre/movie/list?api_key={API_KEY}&language=en-US"
    response = requests.get(url)
    data = response.json()
    genre_mapping = {genre["id"]: genre["name"] for genre in data["genres"]}
    return genre_mapping

def fetch_movie_data():
    genre_mapping = fetch_genre_mapping()
    movies = []
    for page in range(1, NUM_PAGES + 1):
        url = f"{BASE_URL}/discover/movie?api_key={API_KEY}&language=en-US&sort_by=popularity.desc&page={page}"
        response = requests.get(url)
        data = response.json()
        for movie in data.get("results", []):
            genres = ", ".join([genre_mapping.get(genre_id, "Unknown") for genre_id in movie["genre_ids"]])
            movies.append({
                "title": movie["title"],
                "overview": movie["overview"],
                "genres": genres,
                "rating": movie["vote_average"]
            })
        time.sleep(0.25)  # Delay to respect rate limits
    df = pd.DataFrame(movies)
    df.to_csv("movies.csv", index=False)
    print("Movie data fetched and saved.")

if __name__ == "__main__":
    fetch_movie_data()