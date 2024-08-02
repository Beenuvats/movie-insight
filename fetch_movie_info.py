import requests
import pandas as pd

# Replace with your OMDb API key
OMDB_API_KEY = '10901f79'


def get_movie_info(movie_title, omdb_api_key):
    """Fetch IMDb ID and poster URL for a given movie title using OMDb API."""
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={omdb_api_key}"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get('Response') == 'True':
            imdb_id = data.get('imdbID', 'N/A')
            poster_url = data.get('Poster', 'No poster available')
            return imdb_id, poster_url
        else:
            return 'Error', f"Error: {data.get('Error', 'Unknown error')}"
    except Exception as e:
        return 'Error', f"Error fetching movie info: {str(e)}"


def create_movie_info_csv(pickle_file, output_file, omdb_api_key):
    """Create a CSV file mapping movie titles to IMDb IDs and poster URLs."""
    # Load the pickle file
    df_tmdb = pd.read_pickle(pickle_file)

    # Ensure the dataset has a 'title' column
    if 'title' not in df_tmdb.columns:
        raise ValueError("The dataset must contain a 'title' column.")

    # Fetch IMDb IDs and Poster URLs
    movie_info = []
    for title in df_tmdb['title']:
        imdb_id, poster_url = get_movie_info(title, omdb_api_key)
        movie_info.append({'title': title, 'imdb_id': imdb_id, 'poster_url': poster_url})

    # Save to CSV
    df_movie_info = pd.DataFrame(movie_info)
    df_movie_info.to_csv(output_file, index=False)
    print(f"CSV file created: {output_file}")


# Example usage
pickle_file = 'movie.pkl'  # Replace with your TMDb pickle file
output_file = 'movie_info.csv'
create_movie_info_csv(pickle_file, output_file, OMDB_API_KEY)