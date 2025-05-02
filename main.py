from datasets import load_dataset 
import pandas as pd
from data_preparation import load_datasets, merge_datasets, get_sample_dataframe
from plotrewriter import PlotRewriter
# IMDb has a public dataset which comes in handy
##dataset = load_dataset("imdb")
#print(dataset)



def main():
    # Load the datasets
    ratings_df, plots_df = load_datasets()

     # Merge datasets on the 'movie_name' column
    merged_df = merge_datasets(ratings_df, plots_df)
    #print("\nMerged DataFrame Sample:")
    #print(merged_df.head())

    # (Optional) Print samples to verify loading
    #print("Ratings DataFrame Sample:")
    #print(ratings_df.head())
    #print("\nPlot Summaries DataFrame Sample:")
    #print(plots_df.head())
    
   
    
    # Extract a sample for prototyping (500 movies)
   # sample_df = get_sample_dataframe(merged_df, sample_size=500)
    #print("\nSampled DataFrame (500 movies):")
   # print(sample_df.head())
    
    # Instantiate the PlotRewriter from plotrewriter.py
    rewriter = PlotRewriter()
    
    while True:
        # Select a sample movie (for example, the first movie in the sample DataFrame)
        sample_movie = merged_df.sample(n=1).iloc[0] #picks a movie at random instead of in a batch
        movie_name = sample_movie['movie_name']
        movie_summary = sample_movie['movie_summary']
        rating = sample_movie['movie_rating']
        
        print("\nOriginal Movie Information:")
        print("Name:", movie_name)
        print("Rating:", rating)
        print("Summary:", movie_summary)
        
        # Generate the alternate plot ending using the rewriter
        new_ending = rewriter.rewrite_plot(movie_name, movie_summary, rating)
        print("\nAlternate Plot Ending:")
        print(new_ending)

        #ask user whetehr to generate a new plot
        user_choice = input("\nWould you like to generate a rewriting for another movie? (y/n): ").lower()
        if user_choice != "y":
            break

if __name__ == '__main__':
    main()
