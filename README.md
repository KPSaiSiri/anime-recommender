# anime-recommender
# 🎌 OtakuMatch – Anime Recommendation System

OtakuMatch is a personalized anime recommendation system built with **Streamlit**, powered by **cosine similarity** and user ratings.

## 🌟 Features

- 🔍 Search anime by title
- 🎭 Filter by genre
- 🎯 Recommend similar anime using ML
- 💬 Rate and comment your favorites
- 🌑 Toggle between light/dark mode
- 🎲 Surprise Me! button
- 📊 Display top-rated anime

## 🚀 Built With

- Python, Streamlit
- scikit-learn, pandas, numpy
- Anime dataset from [Kaggle](https://www.kaggle.com/datasets)

## 💡 How it Works

- TF-IDF or CountVectorizer is used on anime descriptions.
- Cosine similarity helps suggest similar anime.
- Ratings and genres personalize your feed.

## 🛠️ Run Locally

```bash
git clone https://github.com/KPSaiSiri/anime-recommender.git
cd anime-recommender
pip install -r requirements.txt
streamlit run anime_app.py
