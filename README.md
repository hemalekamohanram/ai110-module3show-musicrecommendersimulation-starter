# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Real-world recommendation systems combine user behavior signals (plays, skips, likes, watch/listen time) with content features, then run large-scale candidate generation and ranking models to predict what each person is most likely to enjoy next. This simulation uses the same core idea at small scale: translate song attributes and user taste into numeric scores, then rank songs by relevance. My version prioritizes content-based vibe features, especially energy, valence, tempo, mood, and genre.

Checkpoint plan status:

- Expanded dataset: the song catalog in data/songs.csv was expanded from 10 to 18 songs with broader genre and mood coverage.
- Specific taste profile for comparisons:
  - favorite_genre = lofi
  - favorite_mood = chill
  - target_energy = 0.38
  - target_tempo_bpm = 78
  - target_valence = 0.60
  - target_danceability = 0.58
  - target_acousticness = 0.82
  - likes_acoustic = True
- Weighted scoring logic is finalized and ready to implement.

Object features used in this simulation:

- Song: id, title, artist, genre, mood, energy, tempo_bpm, valence, danceability, acousticness
- UserProfile: favorite_genre, favorite_mood, target_energy, target_valence, target_tempo_bpm, likes_acoustic

Algorithm Recipe (weighted content-based scoring):

- Score one song at a time against a user profile.
- Use exact-match bonuses for categorical preferences:
  - +2.0 points for genre match
  - +1.0 point for mood match
- Use closeness-based scoring for numeric preferences so being closer is better:
  - energy_similarity = 1 - abs(song_energy - target_energy)
  - clamp energy_similarity into [0, 1]
  - add up to +2.0 similarity points: +2.0 * energy_similarity
- Final single-song score:
  - score = genre_points + mood_points + energy_points
- Sort songs by total_score descending and return top-k.

Potential biases and limitations to watch:

- Genre-overweight bias: +2.0 genre points may over-prioritize same-genre tracks and miss mood-compatible songs from other genres.
- Narrow-profile bias: a single favorite genre and mood can create repetitive recommendations (filter bubble).
- Feature omission bias: lyrics, language, and cultural context are not modeled, so recommendation quality may feel shallow for some listeners.

Feature choices in this simulator:

- Song fields: genre, mood, energy, tempo_bpm, valence, danceability, acousticness
- User profile fields: favorite_genre, favorite_mood, target_energy, target_valence, target_tempo_bpm, likes_acoustic

Weighting decision (genre vs mood):

- Genre should be worth more than mood at the start because it is a stronger style anchor in this dataset.
- Finalized baseline weighting: genre match = +2.0, mood match = +1.0, energy closeness = up to +2.0.
- This gives both categorical identity (genre/mood) and numeric vibe fit (energy).

Scoring Rule vs Ranking Rule:

- Scoring Rule answers: How good is this one song for this user?
- Ranking Rule answers: Which songs are best when we compare the whole list?
- We need both because a recommender must evaluate each item and then choose an ordered top-k slate.

Prompt used to design the math-based scoring rule:

```text
Scoring Logic Design: help me finalize a point-based scoring rule for my music recommender.
I have song features: genre, mood, energy, tempo_bpm, valence, danceability, acousticness.
I have user preferences: favorite_genre, favorite_mood, target_energy, target_tempo_bpm, target_valence, likes_acoustic.

Please:
1) Critique this baseline recipe:
  - +2.0 points for genre match
  - +1.0 point for mood match
  - energy_similarity = 1 - abs(song_energy - target_energy)
  - energy_points = 2.0 * clamp(energy_similarity, 0, 1)
2) Explain if this can clearly separate intense rock from chill lofi.
3) Suggest one improved weighting variant if this baseline is too narrow.
4) Show one worked example score for a single song.
5) Explain why we need both scoring (single song) and ranking (ordered top-k list).
```

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Paste a sample of your recommender's output here as a text block so a reader can see what it produces:

```
Loaded songs: 18

Top recommendations

------------------------------------------------------------------------
Rank  Title                   Score     Reasons
------------------------------------------------------------------------
1     Sunrise City            4.96      genre match (+2.0), mood match (+1.0), energy closeness (+1.96)
2     Gym Hero                3.74      genre match (+2.0), energy closeness (+1.74)
3     Rooftop Lights          2.92      mood match (+1.0), energy closeness (+1.92)
4     Night Drive Loop        1.90      energy closeness (+1.90)
5     Solar Steps             1.88      energy closeness (+1.88)
------------------------------------------------------------------------
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



