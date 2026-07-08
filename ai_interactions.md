# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I asked the agent to extend my recommender with advanced song features, multiple scoring modes, a diversity penalty, and cleaner terminal output while keeping the code modular.

**Prompts used:**

- "Add 5+ advanced attributes to songs.csv (popularity, decade, detailed mood tags, instrumentalness, speechiness, language, explicit) and update loading/scoring logic."
- "Create switchable scoring modes like genre-first, mood-first, and energy-focused using a simple modular design pattern."
- "Implement a diversity rule: penalize songs if the artist already appears in selected top results."
- "Format terminal output as a readable ASCII table including score reasons."

**What did the agent generate or change?**

- Edited `data/songs.csv` to add 7 new columns and values for all 18 songs.
- Updated `src/recommender.py` to:
	- parse the new features from CSV,
	- add mode-specific scoring weights,
	- score advanced features (popularity, decade, detailed mood, instrumentalness, speechiness, language, explicit preference),
	- apply a diversity penalty for repeated artists/genres in top-k selection.
- Updated `src/main.py` to run multiple profiles with multiple scoring modes and print a wider summary table with reasons.
- Ran `python -m src.main` with the local Python executable to verify output.

**What did you verify or fix manually?**

I manually verified the CSV schema and confirmed numeric conversions are valid (int/float/bool). I checked that each scoring mode changes ranking behavior and that diversity penalties appear in the explanation text. I also reviewed edge-case outputs to make sure the model was not crashing when preferences conflict.

---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

Strategy pattern (lightweight version).

**How did AI help you brainstorm or implement it?**

AI suggested separating scoring logic by mode so each strategy can have its own weight profile while reusing one ranking pipeline. That made it easy to switch from `genre_first` to `mood_first` or `energy_focused` without rewriting the full function.

**How does the pattern appear in your final code?**

In `src/recommender.py`, mode-specific behavior is encapsulated in `MODE_WEIGHTS` and selected through `_score_song_with_mode(...)`. `recommend_songs(...)` uses the chosen mode as a strategy input and then applies a shared ranking + diversity step.
