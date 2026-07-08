# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

MoodMatch Mini 1.0

---

## 2. Intended Use  

Goal / Task: This model suggests songs from a small catalog based on a user taste profile. It predicts which songs feel closest to the user vibe.

Intended use: classroom exploration and learning how recommendation logic works.

Non-intended use: real production recommendations, mental health mood detection, or high-stakes user profiling.

---

## 3. How the Model Works  

Algorithm summary: For each song, I give points for genre match and mood match. Then I add energy closeness points based on how near the song energy is to the user target. After scoring every song, I sort from highest to lowest and return top 5. This makes the model easy to explain, but also easy to bias if one feature weight is too strong.

---

## 4. Data  

Data used: 18 songs in songs.csv.

Main features: genre, mood, energy, tempo_bpm, valence, danceability, acousticness.

I expanded the starter data from 10 to 18 songs with more genres and moods.

Limits: still a tiny catalog, only one row per song, and no lyrics, language, or listening history.

---

## 5. Strengths  

The model works well when user intent is clear, like High-Energy Pop or Chill Lofi. Top results usually match expected vibe. The explanations are also useful because I can see exactly why a song ranked high.

---

## 6. Limitations and Bias 

One weakness I found is that the current scoring overweights energy closeness, which can create an "energy bubble" and ignore style intent. In my edge-case test (rock + intense + very low energy), the recommender mostly returned low-energy chill tracks instead of intense tracks, which felt unintuitive. This means users with conflicting preferences can get recommendations that match a single numeric feature but miss the overall vibe they likely want. The model also ignores important signals like lyrics, language, and context, so it can flatten different listening goals into similar outputs.

---

## 7. Evaluation  

I tested four profiles: High-Energy Pop, Chill Lofi, Deep Intense Rock, and an edge case (rock + intense + very low energy). I looked at whether top songs matched the intended vibe, not just one feature.

What surprised me: "Gym Hero" appeared for multiple profiles because it has very high energy, so the score can stay strong even when genre is not a perfect match. This showed me that energy can dominate results when weights are high.

High-Energy Pop vs Chill Lofi: Pop recommendations moved toward upbeat, high-energy tracks, while Chill Lofi moved toward softer, slower tracks like "Library Rain." This makes sense because both mood and energy targets changed.

Chill Lofi vs Deep Intense Rock: Chill Lofi favored calm tracks, while Deep Intense Rock pushed "Storm Runner" to the top because both genre and mood matched intense preferences.

Deep Intense Rock vs Edge Case (intense + low energy): The edge case shifted away from intense rock toward low-energy songs. That change makes sense mathematically, but it also shows a weakness: the model can over-follow energy and miss overall style intent.

---

## 8. Future Work  

Ideas for improvement:

- Rebalance weights so energy does not dominate every profile.
- Add a diversity rule so top 5 is not all same style.
- Add secondary preferences (for example, second favorite genre or mood).

---

## 9. Personal Reflection  

My biggest learning moment was seeing how small weight changes can totally change outputs. A simple rule can feel smart, but it can also lock into one feature and miss the bigger vibe. AI tools helped me move faster on structure and debugging, but I still had to check logic with real test profiles because some suggestions looked good in theory but gave weird rankings. I was surprised that a basic scoring model still felt like a real recommender when the reasons were printed clearly. If I keep going, I want to add diversity controls and a second-layer rerank step so recommendations feel less repetitive.
