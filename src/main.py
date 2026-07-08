"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Default profile used for quick verification.
    user_prefs = {
        "favorite_genre": "pop",
        "favorite_mood": "happy",
        "target_energy": 0.80,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations\n")
    print("-" * 72)
    print(f"{'Rank':<6}{'Title':<24}{'Score':<10}Reasons")
    print("-" * 72)
    for idx, rec in enumerate(recommendations, start=1):
        song, score, explanation = rec
        print(f"{idx:<6}{song['title']:<24}{score:<10.2f}{explanation}")
    print("-" * 72)


if __name__ == "__main__":
    main()
