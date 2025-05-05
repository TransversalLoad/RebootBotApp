# test_ratings.py
from data_preparation import DataLoader
from plotrewriter import PlotRewriter
from rating_predictor import RatingPredictor
import gradio as gr
import os

# Insert needed path here for RebootBot\Movies shivang
predictor = RatingPredictor(r"C:\Users\wkacc\Documents\University\SWE Y4\Shivang\Assignment 1\RebootBot\Datasets\Movies")

# Train and save the model, uncomment if running on new system for first time
# predictor.train_model()

# Test prediction
test_plot = "A man ran to the moon, the end. "
predicted_rating = predictor.guess_rating(test_plot)
print(f"Predicted rating for your plot: {predicted_rating}/10")



#if __name__ == "__main__":
  # For first time setup 
  # RatingPredictor(r"C:\Users\wkacc\Documents\University\SWE Y4\Shivang\Assignment 1\RebootBot\Datasets\Movies").train_model()
  
