from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import spacy
from collections import Counter

app = Flask(__name__)

print("Starting Flask app...")
import sys
print("Python version:", sys.version)

# Load data and models
print("Loading data...")
df = pd.read_csv("movies_cleaned.csv")
print("Data loaded successfully.")
print("Loading embeddings...")
embeddings = np.load("embeddings.npy")
print("Embeddings loaded successfully.")
print("Loading SentenceTransformer model...")
sentence_model = SentenceTransformer('all-mpnet-base-v2')
print("SentenceTransformer model loaded successfully.")
print("Loading spaCy model...")
nlp = spacy.load("en_core_web_sm")
print("spaCy model loaded successfully.")

# Conversation states
states = {}

def extract_keywords(text):
    doc = nlp(text.lower())
    keywords = [token.text for token in doc if token.pos_ in ["NOUN", "ADJ", "VERB"] and not token.is_stop]
    entities = [ent.text.lower() for ent in doc.ents]
    return list(set(keywords + entities))

def format_movie_recommendations(recommendations):
    """Format movie recommendations for better display in chat"""
    if not recommendations:
        return "Sorry, I couldn't find any matching movies. Would you like to try a different story or genre?"
    
    response = "🎬 <strong>Here are some movies you might enjoy:</strong><br><br>"
    
    for i, movie in enumerate(recommendations, 1):
        title = movie.get('title', 'Unknown Title')
        rating = movie.get('rating', 'N/A')
        
        # Add star rating visualization
        if isinstance(rating, (int, float)) and rating > 0:
            stars = "⭐" * min(int(rating), 5)  # Cap at 5 stars
            rating_display = f"{rating}/10 {stars}"
        else:
            rating_display = "Not rated"
        
        response += f"<div style='margin-bottom: 12px; padding: 8px; background: rgba(255,255,255,0.05); border-radius: 8px; border-left: 3px solid #4ecdc4;'>"
        response += f"<strong style='color: #4ecdc4;'>{i}. {title}</strong><br>"
        response += f"<span style='color: #ffb74d;'>Rating: {rating_display}</span>"
        response += f"</div>"
    
    response += "<br>Would you like more recommendations or want to try a different search?"
    return response

def recommend_by_story(user_story, preferred_genre=None):
    print("Processing story:", user_story)
    user_embedding = sentence_model.encode([user_story])
    similarities = cosine_similarity(user_embedding, embeddings)[0]
    user_keywords = extract_keywords(user_story)
    
    keyword_scores = []
    for overview in df["overview"]:
        if pd.isna(overview):
            keyword_scores.append(0)
            continue
        overview_keywords = extract_keywords(overview)
        common_keywords = len(set(user_keywords) & set(overview_keywords))
        keyword_scores.append(common_keywords / (len(user_keywords) + 1))
    
    combined_scores = 0.7 * similarities + 0.3 * np.array(keyword_scores)
    
    if preferred_genre:
        valid_indices = df["genres"].str.contains(preferred_genre, case=False, na=False)
        combined_scores = combined_scores * valid_indices
    else:
        valid_indices = np.ones(len(df), dtype=bool)
    
    top_indices = combined_scores.argsort()[-5:][::-1]
    top_df_indices = df[valid_indices].index[top_indices]
    recommendations = df.loc[top_df_indices][["title", "rating"]].to_dict(orient="records")
    print("Recommendations:", recommendations)
    return recommendations

def recommend_by_genre_rating(genre, min_rating):
    filtered_df = df[df["genres"].str.contains(genre, case=False, na=False) & (df["rating"] >= min_rating)]
    return filtered_df.sort_values(by="rating", ascending=False).head(5)[["title", "rating"]].to_dict(orient="records")

def process_message(user_id, message):
    message = message.lower().strip()
    print(f"Processing message for user {user_id}: '{message}'")
    if user_id not in states:
        states[user_id] = {"step": "initial", "data": {}}
        print(f"New state created for user {user_id}: {states[user_id]}")

    state = states[user_id]
    print(f"Current state: {state}")
    
    if state["step"] == "initial":
        if "story" in message:
            state["step"] = "story_input"
            print("Transitioning to story_input")
            return "Great! Please describe the story you're interested in. For example:<br><br>🎭 <em>\"A story about time travel and saving the world\"</em><br>🎭 <em>\"A romantic comedy set in a small town\"</em><br>🎭 <em>\"An action movie with superheroes\"</em>"
        elif "genre" in message:
            state["step"] = "genre_input"
            print("Transitioning to genre_input")
            return "Awesome! What genre do you like?<br><br>Popular genres include:<br>🎬 Action • Adventure • Comedy • Drama<br>🎬 Horror • Romance • Sci-Fi • Thriller<br>🎬 Fantasy • Mystery • Animation • Crime"
        else:
            print("Initial prompt sent")
            return "Hi! I can help you find amazing movies in two ways:<br><br>📖 <strong>Story-based:</strong> Describe what kind of story you want to watch<br>🎪 <strong>Genre & Rating:</strong> Tell me your favorite genre and minimum rating<br><br>Just say <strong>'story'</strong> or <strong>'genre'</strong> to get started!"

    elif state["step"] == "story_input":
        print("Received story input")
        state["data"]["story"] = message
        if len(message.split()) < 5:
            state["step"] = "clarify_genre"
            print("Story too short, transitioning to clarify_genre")
            return "That's a good start! Could you add a bit more detail about the story, or tell me a preferred genre to help narrow it down?<br><br>For example: <em>\"Action\"</em>, <em>\"Comedy\"</em>, <em>\"Drama\"</em>, etc."
        recommendations = recommend_by_story(message)
        state["step"] = "initial"
        print(f"Recommendations generated: {recommendations}")
        return format_movie_recommendations(recommendations)

    elif state["step"] == "clarify_genre":
        print("Received genre clarification")
        state["data"]["genre"] = message
        recommendations = recommend_by_story(state["data"]["story"], message)
        state["step"] = "initial"
        print(f"Recommendations generated: {recommendations}")
        return format_movie_recommendations(recommendations)

    elif state["step"] == "genre_input":
        print("Received genre input")
        state["data"]["genre"] = message
        state["step"] = "rating_input"
        return f"Perfect! You chose <strong>{message.title()}</strong> 🎬<br><br>What's the minimum rating you'd like? (1.0 - 10.0)<br><br>💡 <em>Tip: 7.0+ for highly rated movies, 8.0+ for exceptional ones!</em>"

    elif state["step"] == "rating_input":
        print("Received rating input")
        try:
            min_rating = float(message)
            if min_rating < 1.0 or min_rating > 10.0:
                return "Please enter a rating between 1.0 and 10.0 (e.g., 7.5)"
            
            genre = state["data"]["genre"]
            recommendations = recommend_by_genre_rating(genre, min_rating)
            state["step"] = "initial"
            print(f"Recommendations generated: {recommendations}")
            
            if recommendations:
                response = f"🎯 <strong>{genre.title()} movies with rating {min_rating}+ :</strong><br><br>"
                response += format_movie_recommendations(recommendations).replace("🎬 <strong>Here are some movies you might enjoy:</strong><br><br>", "")
            else:
                response = f"Sorry, I couldn't find any <strong>{genre.title()}</strong> movies with a rating of {min_rating}+ 😔<br><br>Try a lower rating or different genre?"
            
            return response
        except ValueError:
            return "Please enter a valid number for the rating (e.g., 7.0, 8.5, 9.2)"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    print("Received chat request")
    data = request.get_json()
    print("Request data:", data)
    user_id = data.get("user_id", "default")
    message = data.get("message")
    if not message:
        return jsonify({"response": "Please type a message."}), 400
    response = process_message(user_id, message)
    print("Response to send:", response)
    return jsonify({"response": response})

if __name__ == "__main__":
    try:
        print("Initializing server...")
        app.run(debug=True)
    except Exception as e:
        print(f"Error starting server: {e}")