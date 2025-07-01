import requests
from django.shortcuts import render,redirect

TMDB_API_KEY = '92d06e0db8dc5a1c00261b77307dca1b'

def search(request):
    return render(request, 'search.html')

def movie_result(request):
    query = request.GET.get('query')
    if not query:
        return redirect('search_page')

    # Search for movie
    search_url = 'https://api.themoviedb.org/3/search/movie'
    search_params = {'api_key': TMDB_API_KEY, 'query': query}
    search_res = requests.get(search_url, params=search_params).json()

    if not search_res['results']:
        return render(request, 'result.html', {'error': 'Movie not found.'})

    movie = search_res['results'][0]
    movie_id = movie['id']

    # Get details, trailer, cast
    details_url = f'https://api.themoviedb.org/3/movie/{movie_id}'
    details_params = {'api_key': TMDB_API_KEY, 'append_to_response': 'videos,credits'}
    details = requests.get(details_url, params=details_params).json()

    # Find trailer
    trailer = None
    for video in details.get('videos', {}).get('results', []):
        if video['type'] == 'Trailer' and video['site'] == 'YouTube':
            trailer = f"https://www.youtube.com/embed/{video['key']}"
            break

    # Handle missing genre or release date
    genres = details.get('genres', [])
    genre_names = ', '.join([g['name'] for g in genres]) if genres else 'N/A'

    context = {
        'title': details.get('title', 'No Title'),
        'rating': details.get('vote_average', 'N/A'),
        'poster': f"https://image.tmdb.org/t/p/w500{details['poster_path']}" if details.get('poster_path') else None,
        'trailer': trailer,
        'overview': details.get('overview', 'No overview available.'),
        'genre': genre_names,
        'release_date': details.get('release_date', 'Unknown'),
        'actors': [cast['name'] for cast in details.get('credits', {}).get('cast', [])[:5]]
    }

    return render(request, 'result.html', context)

