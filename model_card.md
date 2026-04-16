# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  


**SpotAClone 1.0**

---

## 2. Intended Use  

This recommender is designed for classroom exploration and learning, not for real-world music streaming. It generates song recommendations from a small, fixed catalog based on a user's stated preferences for genre, mood, energy, and other features. The system assumes users know what they like and can specify their favorite genre, mood, and target values for features like tempo or valence. It is not intended for commercial use or for users with highly complex or evolving tastes.
---

## 3. How the Model Works  

The model looks at each song's features (like genre, mood, energy, tempo, valence, danceability, and acousticness) and compares them to what the user says they like. If a song matches the user's favorite genre or mood, it gets extra points. The model also checks if the song's numeric features (like tempo or valence) are close to the user's targets, and adds points if they are. For energy, it gives a higher score the closer the song's energy is to the user's target. After scoring all songs, it sorts them and recommends the top ones.

---

## 4. Data  

The dataset contains 20 songs, each with features like genre, mood, artist, energy, tempo, valence, danceability, and acousticness. Genres include pop, rock, jazz, lofi, synthwave, and more, with a variety of moods such as happy, intense, relaxed, and chill. No songs were added or removed from the starter set. Some genres and moods are underrepresented, and there are no songs with extremely high or low values for some features. The catalog is small, so it does not cover the full range of musical tastes or diversity found in real music libraries.

---

## 5. Strengths  

The system works well for users whose preferences match the genres and moods in the dataset. It gives clear, explainable recommendations, and the reasons for each pick are easy to understand. The model is good at finding songs that are close to the user's target energy, tempo, or valence. It is transparent, so users can see exactly why a song was recommended.
---

## 6. Limitations and Bias 

The model struggles with users whose preferences are outside the range of the dataset, such as those who want a genre or mood that isn't present, or an energy level higher than any song in the catalog. It can create "filter bubbles" by always recommending songs from the user's favorite genre or mood, ignoring other good matches. The system does not consider lyrics, artist popularity, or user listening history. One weakness found during experiments is that users with extreme or rare preferences (like very high energy) get only low-scoring, generic recommendations, making the system feel unresponsive for them. The model also does not promote diversity or surprise in its recommendations, so users may see the same types of songs repeatedly.

---


## 7. Evaluation

I tested the recommender using three different user profiles: one with impossible preferences (genre and mood not in the dataset, extreme energy), one with contradictory preferences (high acousticness, high energy, high danceability), and one with realistic but specific preferences (jazz, relaxed mood, high valence, moderate tempo, likes acoustic). For each profile, I checked if the top recommendations matched the user's stated preferences and if the explanations made sense. I also experimented with changing the genre weight, adding tempo and valence to the score, and disabling the mood check to see how the results changed. I was surprised that users with extreme or rare preferences always got low scores and generic recommendations, while users with more typical preferences got clear, relevant results. The experiments helped reveal where the model is strong and where it fails to adapt to unusual user needs.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
