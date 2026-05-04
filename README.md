# 🎵 Music Recommender Simulation

## Project Summary

This is a simple music recommender for learning. It suggests songs from a small list based on what you like, such as genre, mood, and energy. Songs get points for matching your preferences, and the top ones are recommended with a short reason why. The project shows how basic recommenders work and where they can be limited or biased.

---

## How The System Works

This recommender scores each song with simple, rule-based points and then returns the top results. There is no Gaussian weighting or learned model.

Each `Song` uses these features: energy, tempo_bpm, valence, danceability, acousticness, genre, and mood.

Each user profile provides a favorite genre and mood, plus target values for numeric features like energy, tempo, valence, danceability, and acousticness. Favorite artist is optional, and any missing targets are simply skipped.
# StatBuddy

StatBuddy is a Python 3.11+ statistics peer tool that analyzes a user-uploaded CSV, detects a suitable dependent-variable model, asks GitHub Copilot for ranked predictor suggestions, fits the model, and exports an HTML report.

## Folder Structure

```text
├── app.py
├── core/
│   ├── __init__.py
│   ├── statbuddy.py
│   ├── dataset_loader.py
│   ├── dv_analyzer.py
│   └── model_selector.py
├── analysis/
│   ├── __init__.py
│   ├── descriptive_analyzer.py
│   └── model_builder.py
├── ai/
│   ├── __init__.py
│   └── copilot_advisor.py
├── output/
│   ├── __init__.py
│   └── report_generator.py
├── knowledge/
│   └── model_rules.json
├── templates/
│   └── report.html
├── tests/
│   ├── test_dataset_loader.py
│   ├── test_dv_analyzer.py
│   ├── test_model_selector.py
│   ├── test_descriptive_analyzer.py
│   ├── test_model_builder.py
│   └── test_copilot_advisor.py
├── requirements.txt
└── README.md
```

## Setup

Install dependencies with:

```bash
pip install -r requirements.txt
```

## Run

Launch the app with:

```bash
streamlit run app.py
```

## Tests

Run the unit tests with:

```bash
pytest
```