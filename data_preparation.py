import pandas as pd 
import matplotlib.pyplot as plt

# This project relies on two datasets currently, a movies CSV dataset form Kaggle Called "Top 250 Movies"
# and a video game csv called "Metacritic scraped". 
# The prior has a rating column but the latter has a metascore as a percentage, so for simpliciity 
# these will be narrowed to Top 10 before score conversion


# Placing the filepaths
#movies_dataset_path = r"C:\Users\wkacc\Documents\University\SWE Y4\Shivang\Assignment 1\RebootBot\Datasets\Movies\IMDB Top 250 Movies.csv"
#games_dataset_path = r"C:\Users\wkacc\Documents\University\SWE Y4\Shivang\Assignment 1\RebootBot\Datasets\Games\dataset_metacritic_scraper_2025-02-15.csv"


# Loading the datasets, column search commented out for now
#movies_df = pd.read_csv(movies_dataset_path)
#print("Movies dataset loaded. Columns found:", movies_df.columns.tolist())


#games_df = pd.read_csv(games_dataset_path)
#print("Games dataset loaded. Columns found:", games_df.columns.tolist())

#  Filtering for the top 10 for simplicity 
#IMdb is sorted in descending order usually so higher rating movies are shown first
#top_movies_df = movies_df.sort_values(by="rating", ascending=False).head(10)
#print("Top 10 Movies (showing rank, rating, name):")
#print(top_movies_df[["rank", "rating", "name"]])

def load_datasets(ratings_file='Datasets/Movies/movie_names_ratings.csv', 
                  plots_file='Datasets/Movies/movie_plot_summaries.csv'):

#New plan, create movie reboot by ratings alone because finding full movie scripts is hard and has licencing issues
    ratings_df = pd.read_csv(ratings_file)
    plots_df = pd.read_csv(plots_file)
    return ratings_df, plots_df


def merge_datasets(ratings_df, plots_df):
# Inspect the first few rows 
#print("Ratings DataFrame:")
#print(ratings_df.head())
#print("\nPlot Summaries DataFrame:")
#print(plots_df.head())

#using merge to merge them based on name 
    merged_df = pd.merge(ratings_df, plots_df, on='movie_name', how='inner')
    return merged_df
#print("\nMerged DataFrame Sample:")
#print(merged_df.head())

def get_sample_dataframe(merged_df, sample_size=500, random_state=42):
    # Determine the actual sample size: either sample_size or the total number of rows, whichever is smaller.
    actual_sample_size = min(sample_size, len(merged_df))
    sample_df = merged_df.sample(n=actual_sample_size, random_state=random_state)
    return sample_df

#Converting percentage score into a numerric. commented out and swapped with userscore for convenience 
#if games_df['metascore'].dtype == object:
    #games_df['metascore'] = games_df['metascore'].str.rstrip('%')
#games_df['metascore'] = pd.to_numeric(games_df['metascore'], errors='coerce')
#games_df['userscore'] = pd.to_numeric(games_df['userscore'], errors='coerce')

#Same for games
#top_games_df = games_df.sort_values(by="userscore", ascending=False).head(10)
#print("\nTop 10 Games (showing title, metascore, userscore):")
#print(top_games_df[["title", "metascore", "userscore"]])


# TROUBLESHOOT Game dataset doesnt contain a "Ratings" column. Changed Ratings to Rank, Title in IMDb also chanegd to name
# print("Movies DataFrame Columns:", movies_df.columns) 

#Finding the median for both categories
#print("Movie Rating Summary:")
#print(movies_df['rating'].describe())
#
#print("\nGame Userscore Summary:")
#print(games_df['userscore'].describe())


# first attempt at data visualisation
# Visualizing movie ratings
#movies_df['rating'].hist(bins=20, color='skyblue', edgecolor='black')
#plt.title('Distribution of Movie Ratings')
#plt.xlabel('Rating')
#plt.ylabel('Frequency')
#plt.show()

# Visualizing game userscore
##games_df['userscore'].hist(bins=20, color='salmon', edgecolor='black')#
#plt.title('Distribution of Game Userscores')
#plt.xlabel('Userscore')
#plt.ylabel('Frequency')
#
#plt.show()
