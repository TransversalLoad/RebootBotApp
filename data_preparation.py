import pandas as pd
import os

#initial class 
class DataLoader:
    def __init__(self, data_dir, 
                rating_file="movie_names_ratings.csv",  
                summary_file="movie_plot_summaries.csv"):  
        self.rating_path = os.path.join(data_dir, rating_file)
        self.summary_path = os.path.join(data_dir, summary_file)
        
        # check paths are correct and give prompt
        print(f"\n=== VERIFYING PATHS ===")
        print(f"Ratings file exists: {os.path.exists(self.rating_path)}")
        print(f"Summaries file exists: {os.path.exists(self.summary_path)}")


    #merging the datasets 
    def load_and_merge_data(self):
        
        ratings = pd.read_csv(self.rating_path)
        summaries = pd.read_csv(self.summary_path)
        
        # merging based on movie_name
        merged = pd.merge(
            ratings[["movie_name", "movie_rating"]],  
            summaries[["movie_name", "movie_summary"]], 
            on="movie_name", 
            how="inner"
        )
        
        #thispart isnt really needed anymore
        print("\n=== SAMPLE MOVIES ===")
        print(merged[["movie_name", "movie_rating"]].head())
        return merged.dropna().drop_duplicates(subset="movie_name")

    def get_movie_list(self):
        df = self.load_and_merge_data()
        return df["movie_name"].tolist()