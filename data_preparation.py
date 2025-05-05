import pandas as pd
import os

class DataLoader:
    def __init__(self, data_dir, data_file="movie_data.csv"):
        self.data_path = os.path.join(data_dir, data_file)
        
        # Makiing sure dataset is present
        if not os.path.exists(self.data_path):
            raise FileNotFoundError(f"Dataset file missing: {self.data_path}")

    def load_data(self):
        """Load and clean the movie dataset"""
        df = pd.read_csv(self.data_path)
        
    # Cleaning 
        df = df.dropna(subset=['movie_name', 'movie_summary'])  # specifying columns
        df['movie_summary'] = df['movie_summary'].astype(str).str.strip()
        df = df[df['movie_summary'].str.len() > 10]  # shortening output summaries
            
        # Remove empty summaries from dataset 
        df = df[df['movie_summary'].str.len() > 50]
        
        print(f"Loaded {len(df)} valid movie entries")
        return df

    def get_movie_list(self):
        """Get sorted list of movie names"""
        df = self.load_data()
        return sorted(df['movie_name'].unique().tolist())