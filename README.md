# CinePredict

CinePredict is a Flask-based web application delivering AI-powered movie recommendations through an interactive chatbot interface. It leverages SentenceTransformers to encode user story descriptions for semantic similarity matching and spaCy for keyword extraction to enhance recommendation accuracy. Styled with Tailwind CSS, it offers a responsive UI for users to discover films by story or genre/rating preferences.

## Table of Contents

- Features
- Installation
- Usage
- Project Structure
- Technologies Used
- Contributing
- License
- Acknowledgments

## Features

- **AI-Driven Recommendations**: Utilizes SentenceTransformers (`all-mpnet-base-v2`) for semantic similarity and spaCy (`en_core_web_sm`) for keyword extraction to deliver precise movie recommendations.
- **Story-Based Recommendations**: Users can input a movie plot description, and the AI matches it to similar movies using semantic and keyword analysis.
- **Genre & Rating Filters**: Filter movies by preferred genre (e.g., Action, Comedy) and minimum rating (e.g., 7.0).
- **Responsive Interface**: Built with Tailwind CSS for a modern, dark-mode-compatible UI with a clean chatbot design.
- **Interactive Chatbot**: Provides a user-friendly interface for seamless interaction and movie discovery.
- **Data Pipeline**: Includes scripts to fetch movie data from TMDB and generate embeddings for recommendations.

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Node.js (optional, for Tailwind CSS build if not using CDN)
- Git (for cloning the repository)
- TMDB API key (sign up at TMDB to obtain one)

### Setup Instructions

1. **Clone the Repository**

   ```bash
   https://github.com/maheenshkk/ai-powered-chatbot-cinepredict.git
   cd cinepredict
   ```

2. **Create and Activate a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python Dependencies**

   ```bash
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

4. **Fetch Movie Data**

   - Edit `fetch_movie_data.py` to add your TMDB API key:

     ```python
     TMDB_API_KEY = "your_tmdb_api_key_here"  # Replace with your TMDB API key
     ```

   - Run the script to generate `movies_cleaned.csv`:

     ```bash
     python fetch_movie_data.py
     ```

5. **Generate Embeddings**

   - Run the script to generate `embeddings.npy` from `movies_cleaned.csv`:

     ```bash
     python generate_embeddings.py
     ```

6. **Run the Application**

   ```bash
   python app.py
   ```

   - Open your browser and navigate to `http://localhost:5000`.

## Usage

1. **Access the Web App**

   - Visit `http://localhost:5000` to view the CinePredict interface.
   - Browse a grid of featured movies with posters, genres, years, ratings, and summaries.

2. **Interact with the Chatbot**

   - Click the "CinePredict AI" button (bottom-right corner) to open the chatbot modal.
   - Type `story` to get recommendations based on a plot description (e.g., "A hacker discovers a simulated reality").
   - Type `genre` to filter movies by genre (e.g., "Action") and minimum rating (e.g., "7.0").
   - Follow the chatbot prompts to refine your input.

3. **View Recommendations**

   - Recommendations are displayed in a styled container, with each movie listed on a separate line, including title and rating (e.g., "- The Matrix (Rating: 8.7)").
   - The chatbot supports iterative queries, allowing you to try different stories or genres.

## Project Structure

```plaintext
cinepredict/
├── static/
│   └── styles.css           # Custom CSS for recommendation styling
├── templates/
│   └── index.html           # HTML template with Tailwind CSS and jQuery
├── app.py                   # Flask backend with AI recommendation logic
├── fetch_movie_data.py      # Script to fetch movie data and create movies_cleaned.csv
├── generate_embeddings.py   # Script to generate embeddings and create embeddings.npy
├── movies_cleaned.csv       # Movie dataset (generated, not included)
├── embeddings.npy           # Precomputed movie embeddings (generated, not included)
├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

## Technologies Used

- **Backend**:
  - **Flask**: Web framework for routing and rendering templates.
  - **SentenceTransformers (**`all-mpnet-base-v2`**)**: Encodes movie plots for semantic similarity matching.
  - **spaCy (**`en_core_web_sm`**)**: Extracts keywords for enhanced recommendation accuracy.
  - **pandas & numpy**: Handles movie data and embeddings.
  - **scikit-learn**: Computes cosine similarity for recommendations.
  - **requests**: Fetches movie data from the TMDB API.
- **Frontend**:
  - **Tailwind CSS**: Provides responsive, utility-first styling via CDN.
  - **jQuery**: Manages AJAX requests and DOM manipulation for the chatbot.
  - **HTML/CSS/JavaScript**: Structures the UI and handles interactivity.
- **Environment**:
  - Python 3.8+: Runs the backend logic.
  - Browser-compatible: No additional client-side setup required.

## Contributing

We welcome contributions to enhance CinePredict! To contribute:

1. Fork the repository.

2. Create a feature branch:

   ```bash
   git checkout -b feature/your-feature
   ```

3. Commit your changes:

   ```bash
   git commit -m "Add your feature"
   ```

4. Push to the branch:

   ```bash
   git push origin feature/your-feature
   ```

5. Open a pull request on GitHub.

Please adhere to PEP 8 for Python code and include relevant tests or documentation updates.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- Built with Flask, SentenceTransformers, spaCy, and TMDB API.
- Styled using Tailwind CSS for a modern, responsive UI.
- Inspired by movie recommendation systems and datasets like IMDb and TMDB.
