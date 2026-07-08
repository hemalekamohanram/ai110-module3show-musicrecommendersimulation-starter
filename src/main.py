"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def print_recommendations_for_profile(profile_name: str, user_prefs: dict, songs: list, mode: str) -> None:
    """Print top-k recommendations for a single taste profile."""
    recommendations = recommend_songs(user_prefs, songs, k=5, mode=mode, diversity_penalty=True)

    print(f"\nProfile: {profile_name} | Mode: {mode}")
    print("-" * 118)
    print(f"{'Rank':<6}{'Title':<22}{'Artist':<18}{'Genre':<12}{'Score':<8}Reasons")
    print("-" * 118)
    for idx, rec in enumerate(recommendations, start=1):
        song, score, explanation = rec
        print(f"{idx:<6}{song['title']:<22}{song['artist']:<18}{song['genre']:<12}{score:<8.2f}{explanation}")
    print("-" * 118)


def main() -> None:
    songs = load_songs("data/songs.csv") 

    profiles = {
        "High-Energy Pop": ({
            "favorite_genre": "pop",
            "favorite_mood": "happy",
            "target_energy": 0.90,
            "target_popularity": 85,
            "preferred_decade": "2020s",
            "preferred_language": "english",
            "allow_explicit": True,
        }, "genre_first"),
        "Chill Lofi": ({
            "favorite_genre": "lofi",
            "favorite_mood": "chill",
            "target_energy": 0.35,
            "target_instrumentalness": 0.80,
            "target_speechiness": 0.03,
            "preferred_detailed_mood": "study",
            "allow_explicit": False,
        }, "mood_first"),
        "Deep Intense Rock": ({
            "favorite_genre": "rock",
            "favorite_mood": "intense",
            "target_energy": 0.95,
            "target_popularity": 75,
            "preferred_decade": "2010s",
            "allow_explicit": False,
        }, "energy_focused"),
        "Edge Case: Intense + Low Energy": ({
            "favorite_genre": "rock",
            "favorite_mood": "intense",
            "target_energy": 0.20,
            "target_instrumentalness": 0.85,
            "preferred_language": "instrumental",
            "allow_explicit": False,
        }, "energy_focused"),
    }

    for profile_name, profile_config in profiles.items():
        user_prefs, mode = profile_config
        print_recommendations_for_profile(profile_name, user_prefs, songs, mode)


if __name__ == "__main__":
    main()
