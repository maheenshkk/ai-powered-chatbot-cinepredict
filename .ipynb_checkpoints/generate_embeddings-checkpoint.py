import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer

def clean_overview(overview):
    if pd.isna(overview) or overview.strip() == "":
        return None
    # Remove promotional or irrelevant phrases (basic cleaning)
    return overview.strip()

def generate_embeddings():
    model = SentenceTransformer('all-mpnet-base-v2')
    df = pd.read_csv("movies.csv")
    df["overview"] = df["overview"].apply(clean_overview)
    valid_df = df[df["overview"].notna()]
    overviews = valid_df["overview"].tolist()
    embeddings = model.encode(overviews, show_progress_bar=True)
    np.save("embeddings.npy", embeddings)
    valid_df.to_csv("movies_cleaned.csv", index=False)  # Save cleaned dataset
    print("Embeddings generated and saved. Cleaned dataset saved as movies_cleaned.csv.")

if __name__ == "__main__":
    generate_embeddings()