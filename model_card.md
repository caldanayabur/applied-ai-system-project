# StatBuddy Model Card

## 1. Model Overview

StatBuddy is a statistics peer tool for uploaded CSV files. It inspects the dependent variable, suggests predictors, fits a basic statistical model, and exports a shareable HTML report. It is intended for exploratory analysis and lightweight model selection support, not for fully automated scientific inference.

## 2. Pipeline Summary

- `DatasetLoader` reads the CSV and stores dataset metadata.
- `DVAnalyzer` detects the dependent-variable type and computes distribution statistics.
- `ModelSelector` maps the detected type to a statistical model.
- `CopilotAdvisor` suggests predictors with GitHub Copilot SDK support and a correlation fallback.
- `DescriptiveAnalyzer` generates summaries, tables, and plots for predictors.
- `ModelBuilder` builds a statsmodels formula and fits the selected model family.
- `ReportGenerator` compiles the final HTML report.

## 3. Supported Statistical Models

- OLS: Linear regression for continuous outcomes.
- Logit: Logistic regression for binary outcomes.
- Poisson: Count regression for non-negative event counts.
- Negative Binomial: Count regression when variance exceeds the mean.
- Tobit: Censored-outcome support, approximated with OLS in this scaffold.

## 4. AI Component

StatBuddy integrates the GitHub Copilot SDK through `CopilotAdvisor`. The advisor sends a prompt containing the dataset column names and dependent variable name, then requests a ranked predictor list with brief justifications. If the SDK connection fails, StatBuddy falls back to a correlation-based selection strategy.

## 5. Limitations

StatBuddy does not yet support panel data, survival models, or time-series workflows. It also does not perform advanced feature engineering, automated hyperparameter tuning, or robust causal inference.

## 6. Dependencies

- streamlit
- pandas
- numpy
- scipy
- statsmodels
- matplotlib
- seaborn
- jinja2
- github-copilot-sdk
- pytest

I tested the recommender using three different user profiles: one with impossible preferences (genre and mood not in the dataset, extreme energy), one with contradictory preferences (high acousticness, high energy, high danceability), and one with realistic but specific preferences (jazz, relaxed mood, high valence, moderate tempo, likes acoustic). For each profile, I checked if the top recommendations matched the user's stated preferences and if the explanations made sense. I also experimented with changing the genre weight, adding tempo and valence to the score, and disabling the mood check to see how the results changed. I was surprised that users with extreme or rare preferences always got low scores and generic recommendations, while users with more typical preferences got clear, relevant results. The experiments helped reveal where the model is strong and where it fails to adapt to unusual user needs.

---

## 8. Future Work  


If I extended this project, I would swap out all the songs in the dataset for tracks from my own music library. This would let me test the recommender with my real preferences and see if it can actually give good suggestions. I would also look for ways to add more features, handle more complex or specific user tastes, and improve the diversity of recommendations so users don’t always get the same types of songs.

---

## 9. Personal Reflection  


Building this recommender showed me how complex real music apps like Spotify must be, since they serve millions of users and use far more features than my simple system. I learned it’s hard to recommend music to people with very specific tastes. For example, users with extreme preferences only got low-scoring, generic results, which made the system feel unhelpful for them. I also realized how much human judgment still matters, because the model can only use the features it has and might miss what really makes a song enjoyable for someone. I was surprised that even a simple scoring system could still feel somewhat personalized. I also found it important to double-check the changes suggested by AI tools, to make sure the code still made sense.
