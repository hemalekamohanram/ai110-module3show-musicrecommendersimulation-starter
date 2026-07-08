from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv


MODE_WEIGHTS = {
    "balanced": {
        "genre": 1.0,
        "mood": 1.0,
        "energy": 4.0,
        "popularity": 1.2,
        "instrumentalness": 0.8,
        "speechiness": 0.8,
        "decade": 0.8,
        "detailed_mood": 0.8,
        "language": 0.5,
        "explicit": 0.5,
    },
    "genre_first": {
        "genre": 2.5,
        "mood": 0.8,
        "energy": 2.0,
        "popularity": 1.0,
        "instrumentalness": 0.6,
        "speechiness": 0.6,
        "decade": 0.8,
        "detailed_mood": 0.6,
        "language": 0.4,
        "explicit": 0.4,
    },
    "mood_first": {
        "genre": 0.8,
        "mood": 2.5,
        "energy": 2.0,
        "popularity": 1.0,
        "instrumentalness": 0.6,
        "speechiness": 0.6,
        "decade": 0.8,
        "detailed_mood": 1.0,
        "language": 0.4,
        "explicit": 0.4,
    },
    "energy_focused": {
        "genre": 0.6,
        "mood": 0.8,
        "energy": 5.0,
        "popularity": 1.0,
        "instrumentalness": 0.8,
        "speechiness": 0.8,
        "decade": 0.6,
        "detailed_mood": 0.6,
        "language": 0.4,
        "explicit": 0.4,
    },
}

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from CSV into typed dictionaries."""
    songs: List[Dict] = []

    with open(csv_path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            songs.append(
                {
                    "id": int(row["id"]),
                    "title": row["title"],
                    "artist": row["artist"],
                    "genre": row["genre"],
                    "mood": row["mood"],
                    "energy": float(row["energy"]),
                    "tempo_bpm": float(row["tempo_bpm"]),
                    "valence": float(row["valence"]),
                    "danceability": float(row["danceability"]),
                    "acousticness": float(row["acousticness"]),
                    "popularity_score": int(row["popularity_score"]),
                    "release_decade": row["release_decade"],
                    "detailed_mood_tag": row["detailed_mood_tag"],
                    "instrumentalness": float(row["instrumentalness"]),
                    "speechiness": float(row["speechiness"]),
                    "language": row["language"],
                    "explicit": bool(int(row["explicit"])),
                }
            )

    print(f"Loaded songs: {len(songs)}")
    return songs

def _closeness(value: float, target: float, span: float = 1.0) -> float:
    """Return a normalized similarity score in the [0, 1] range."""
    similarity = 1.0 - (abs(value - target) / span)
    return max(0.0, min(1.0, similarity))


def _score_song_with_mode(user_prefs: Dict, song: Dict, mode: str) -> Tuple[float, List[str]]:
    """Apply a mode-specific scoring strategy to one song."""
    score = 0.0
    reasons: List[str] = []
    weights = MODE_WEIGHTS.get(mode, MODE_WEIGHTS["balanced"])

    # Support either naming convention used in the project prompts.
    favorite_genre = user_prefs.get("favorite_genre", user_prefs.get("genre"))
    favorite_mood = user_prefs.get("favorite_mood", user_prefs.get("mood"))
    target_energy = float(user_prefs.get("target_energy", user_prefs.get("energy", 0.5)))
    target_popularity = float(user_prefs.get("target_popularity", 70))
    target_instrumentalness = float(user_prefs.get("target_instrumentalness", 0.4))
    target_speechiness = float(user_prefs.get("target_speechiness", 0.08))
    preferred_decade = user_prefs.get("preferred_decade")
    preferred_detail = user_prefs.get("preferred_detailed_mood")
    preferred_language = user_prefs.get("preferred_language")
    allow_explicit = user_prefs.get("allow_explicit")

    if favorite_genre and song.get("genre") == favorite_genre:
        score += weights["genre"]
        reasons.append(f"genre match (+{weights['genre']:.1f})")

    if favorite_mood and song.get("mood") == favorite_mood:
        score += weights["mood"]
        reasons.append(f"mood match (+{weights['mood']:.1f})")

    energy_value = float(song.get("energy", 0.0))
    energy_similarity = _closeness(energy_value, target_energy)
    energy_points = weights["energy"] * energy_similarity
    score += energy_points
    reasons.append(f"energy closeness (+{energy_points:.2f})")

    popularity_similarity = _closeness(float(song.get("popularity_score", 50)), target_popularity, span=100.0)
    popularity_points = weights["popularity"] * popularity_similarity
    score += popularity_points
    reasons.append(f"popularity fit (+{popularity_points:.2f})")

    instrumental_similarity = _closeness(float(song.get("instrumentalness", 0.0)), target_instrumentalness)
    instrumental_points = weights["instrumentalness"] * instrumental_similarity
    score += instrumental_points
    reasons.append(f"instrumental fit (+{instrumental_points:.2f})")

    speech_similarity = _closeness(float(song.get("speechiness", 0.0)), target_speechiness)
    speech_points = weights["speechiness"] * speech_similarity
    score += speech_points
    reasons.append(f"speech fit (+{speech_points:.2f})")

    if preferred_decade and song.get("release_decade") == preferred_decade:
        score += weights["decade"]
        reasons.append(f"decade match (+{weights['decade']:.1f})")

    if preferred_detail and song.get("detailed_mood_tag") == preferred_detail:
        score += weights["detailed_mood"]
        reasons.append(f"detailed mood match (+{weights['detailed_mood']:.1f})")

    if preferred_language and song.get("language") == preferred_language:
        score += weights["language"]
        reasons.append(f"language match (+{weights['language']:.1f})")

    if allow_explicit is not None and bool(song.get("explicit")) == bool(allow_explicit):
        score += weights["explicit"]
        reasons.append(f"explicit preference fit (+{weights['explicit']:.1f})")

    return score, reasons


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song and return (score, reasons)."""
    mode = user_prefs.get("mode", "balanced")
    return _score_song_with_mode(user_prefs, song, mode)

def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    mode: str = "balanced",
    diversity_penalty: bool = True,
) -> List[Tuple[Dict, float, str]]:
    """Rank songs by mode-aware scores and optionally apply diversity penalties."""
    scored: List[Tuple[Dict, float, List[str]]] = []

    for song in songs:
        score, reasons = _score_song_with_mode(user_prefs, song, mode)
        scored.append((song, score, reasons))

    if not diversity_penalty:
        ranked = sorted(scored, key=lambda item: item[1], reverse=True)
        return [(song, score, ", ".join(reasons)) for song, score, reasons in ranked[:k]]

    selected: List[Tuple[Dict, float, str]] = []
    selected_artists = set()
    selected_genres = set()
    remaining = scored.copy()
    artist_penalty = 1.0
    genre_penalty = 0.6

    while remaining and len(selected) < k:
        best_index = -1
        best_adjusted_score = float("-inf")
        best_reason = ""

        for idx, (song, base_score, reasons) in enumerate(remaining):
            penalty = 0.0
            penalty_tags: List[str] = []

            if song.get("artist") in selected_artists:
                penalty += artist_penalty
                penalty_tags.append(f"artist repeat penalty (-{artist_penalty:.1f})")

            if song.get("genre") in selected_genres:
                penalty += genre_penalty
                penalty_tags.append(f"genre repeat penalty (-{genre_penalty:.1f})")

            adjusted_score = base_score - penalty
            explanation = ", ".join(reasons + penalty_tags)

            if adjusted_score > best_adjusted_score:
                best_adjusted_score = adjusted_score
                best_index = idx
                best_reason = explanation

        best_song, _, _ = remaining.pop(best_index)
        selected.append((best_song, best_adjusted_score, best_reason))
        selected_artists.add(best_song.get("artist"))
        selected_genres.add(best_song.get("genre"))

    return selected
