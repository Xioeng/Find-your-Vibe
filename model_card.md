# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

 **FindYourVibe 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

This model is designed to recommend songs from a small catalog based on a user's preferred genre, mood, energy level, and acoustic preference. It is intended for classroom exploration and learning about recommender systems, not for real users or commercial use. However, it implements basic principles of recommendation that could be applied in a more complex system. It contains a small dataset with different genres and moods for the user to interact with and see how the recommendations change based on their preferences.

---

## 3. How the Model Works  

This model scores based in a given user's preferences for genre, mood, energy level, and acoustic preference. It calculates a score for each song in the catalog based on how well it matches the user's preferences. The scoring logic considers the following features of each song:
- Genre: It checks if the song's genre matches the user's favorite genre.
- Mood: It checks if the song's mood matches the user's favorite mood.
- Energy: It calculates how close the song's energy level is to the user's target energy level
- Acoustic: It checks if the song's acousticness matches the user's preference for acoustic music.
- Danceability: It considers the song's danceability as a factor in the score. The final score is a weighted combination of these factors, with genre and mood having the highest weights (0.35, 0.30, 0.20, 0.10, 0.05 respectively).

Hence, the songs with the highest scores are recommended to the user.


---

## 4. Data  

The dummy data that the model uses is stored in `data/songs.csv`. It contains 200 songs with various features such as genre, mood, energy level, acousticness, and danceability.

More explicitly the dataset includes for each song:
- id - Song identifier
- title - Song title
- artist - Artist name
- genre - Music genre
- mood - Emotional mood
- energy - Energy level (0.0-1.0)
- tempo_bpm - Beats per minute
- valence - Musical positivity (0.0-1.0)
- danceability - How danceable (0.0-1.0)
- acousticness - Acoustic level (0.0-1.0)

It includes: 
### Unique Genres (16 total)
- pop
- lofi
- rock
- ambient
- jazz
- synthwave
- reggae
- folk
- hip-hop
- electronic
- indie pop
- soul
- rap
- acoustic
- indie
- techno
### Unique Moods (8 total)
- happy
- chill
- intense
- focused
- relaxed
- moody
- peaceful

---

## 5. Strengths  

The system has an intuitive scoring mechanism that combines multiple song features to generate recommendations. It allows for a variety of user preferences, including genre, mood, energy level, and acoustic preference. The use of a weighted scoring system enables the model to prioritize certain features over others, which can lead to more personalized recommendations. 

---

## 6. Limitations and Bias 

The system does not hold the user's history or set of preferences. This could augment dramatically the quality and relevance of the recommendations. Even a list of songs that the user has liked or disliked in the past would allow the system to learn from the user's interactions and improve its recommendations over time.

Since the weights are fixed and most of the scoring accounts for the genre and mood the system cannot suggest songs that are outside of the user's genre and mood preferences. 

---

## 7. Evaluation  

As shown in the README, the system was evaluated using a set of test cases that check if the recommendations align with the user's preferences. The tests cover various scenarios, including users with different genre and mood preferences, energy levels, and acoustic preferences. The results support the claim that the system can generate recommendations that are relevant to the user's preferences, but also show that it can narrow too much the scope of the recommendations, mostly in larger catalogs.

---

## 8. Future Work  

Future work should include a different scoring mechanism or one more adaptable, eventually this would require to make the user preferences to be more diverse, probably obtaining a set of songs and from them creating a heuristic that allows to determine the user's preferences or weights to be applied to the different features so eventually each user would have a different scoring mechanism.

On the other hand, more scoring algorithms should be tested, for example, a more complex one that considers the similarity between genres and moods. Moreover, it would be useful to include data that is fetched from an API, such as Spotify, to have a more realistic dataset and be able to test the system with a larger catalog of songs.

Finally, an interactive but simple user interface could be developed to allow users to input their preferences and see the recommendations, probably in a web-based format like streamlit.

