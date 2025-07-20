# ✅ Always put imports at the top
import pandas as pd
import streamlit as st
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import random
import os

# ✅ Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# 🔐 Login form
if not st.session_state.logged_in:
    username = st.text_input("👤 Username")
    password = st.text_input("🔑 Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state.logged_in = True
            st.success("✅ Logged in successfully!")
            st.rerun()  # 🔁 Refresh the app
        else:
            st.error("❌ Wrong username or password")
    st.stop()


# ✅ Load the anime dataset
anime_df = pd.read_csv("anime_standalone.csv")

# ✅ Clean and prepare the data
anime_df['num_episodes'] = pd.to_numeric(anime_df['num_episodes'], errors='coerce').fillna(0).astype(int)
anime_df['genres'] = anime_df['genres'].fillna('')
all_genres = sorted(set(g for genre_list in anime_df['genres'] for g in genre_list.split(', ')))

# ✅ TF-IDF and cosine similarity
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(anime_df['genres'])
cosine_sim = cosine_similarity(tfidf_matrix, tfidf_matrix)
indices = pd.Series(anime_df.index, index=anime_df['title']).drop_duplicates()

# ✅ Recommendation function
def get_recommendations(title, num=5, genre_filter="All"):
    idx = indices.get(title)
    if idx is None:
        return pd.DataFrame()
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    anime_indices = [i[0] for i in sim_scores if genre_filter == "All" or genre_filter in anime_df.iloc[i[0]]['genres']]
    return anime_df.iloc[anime_indices[1:num+1]][['title', 'genres', 'mean', 'image', 'num_episodes', 'rank']]

# ✅ Streamlit App UI
st.title("🎌 OtakuMatch – Anime Recommender System")
st.markdown("✨ Welcome to OtakuMatch! Find your next favorite anime based on genre similarity!")

# Dark mode toggle (this is visual only unless styled fully via CSS)
dark_mode = st.checkbox("🌙 Dark Mode")
if dark_mode:
    st.markdown("""
        <style>
            body {
                background-color: #0E1117;
                color: white;
            }
        </style>
    """, unsafe_allow_html=True)

# Tabs for clean layout
tab1, tab2, tab3 = st.tabs(["🎯 Recommend", "📈 Top Rated", "📝 Rate & Comment"])


# ✅ Show Top Rated Anime
st.subheader("🏆 Top-Rated Anime")
top_rated = anime_df.sort_values(by='mean', ascending=False).head(3)
for _, row in top_rated.iterrows():
    st.image(row['image'], width=150)
    st.markdown(f"**{row['title']}** – ⭐ {row['mean']}")

# ✅ Genre Filter Dropdown
selected_genre = st.selectbox("🎭 Filter by Genre (Optional):", ["All"] + all_genres)

# ✅ Input and Surprise Me Button
col1, col2 = st.columns([3, 1])
with col1:
    user_input = st.text_input("🎥 Type an anime title you liked:")
with col2:
    if st.button("🎲 Surprise Me!"):
        user_input = random.choice(anime_df['title'].unique())
        st.success(f"🎉 You got: {user_input}")

# ✅ Number of Recommendations
num_recs = st.slider("🎯 How many anime recommendations?", 1, 10, 5)

# ✅ Tabs for layout
tab1, tab2 = st.tabs(["🎬 Recommendations", "📈 Top Rated"])

with tab1:
    if user_input:
        recommendations = get_recommendations(user_input, num=num_recs, genre_filter=selected_genre)
        if not recommendations.empty:
            st.subheader("🍿 Recommended Anime:")
            for _, row in recommendations.iterrows():
                st.image(row['image'], width=200)
                st.markdown(f"""
                ### 🍥 {row['title']}
                **🎭 Genres:** {row['genres']}  
                **⭐ Score:** {row['mean']}  
                **🎬 Episodes:** {row['num_episodes']}  
                **🏅 Rank:** {row['rank']}
                """)
                # ✅ Feedback area
                user_rating = st.slider(f"Rate {row['title']} (1-5 stars)", 1, 5, 3, key=row['title'] + "_rating")
                user_comment = st.text_area(f"💬 Your comment for {row['title']}:", key=row['title'] + "_comment")
                if st.button(f"✅ Submit Feedback for {row['title']}", key=row['title'] + "_submit"):
                    st.success(f"Thanks! You rated {row['title']} ⭐ {user_rating} stars.")
                    st.info(f"📝 Your comment: {user_comment}")
                st.markdown("---")
        else:
            st.warning("Anime not found. Please check spelling and try again.")
st.markdown("### ✨ Leave a Rating & Comment")

selected_anime = st.selectbox("Choose an anime to rate", anime_df['title'].unique())


rating = st.slider("Your rating (1 = bad, 5 = amazing)", 1, 5)
comment = st.text_area("Any thoughts or comment?")

feedback_file = "feedback_data.csv"

# Load existing feedback or create new DataFrame
if os.path.exists(feedback_file):
    feedback_df = pd.read_csv(feedback_file)
else:
    feedback_df = pd.DataFrame(columns=["anime", "rating", "comment"])

# Streamlit form
with st.form("feedback_form"):
    selected_anime = st.selectbox("Choose an anime to rate", anime_data['title'].unique())
    user_rating = st.slider("Your rating (1 = bad, 5 = amazing)", 1, 5, 3)
    user_comment = st.text_input("Any thoughts or comment?")
    submit = st.form_submit_button("Submit Feedback")

    if submit:
        new_feedback = {
            "anime": selected_anime,
            "rating": user_rating,
            "comment": user_comment
        }
        # Add and save to CSV
        feedback_df = pd.concat([feedback_df, pd.DataFrame([new_feedback])], ignore_index=True)
        feedback_df.to_csv(feedback_file, index=False)
        st.success("✅ Thanks for your feedback!")