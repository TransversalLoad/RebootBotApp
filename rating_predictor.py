import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestRegressor
import joblib
import os

# Predicts user movie rating from given summary 
class RatingPredictor:
    def __init__(self, data_dir):
    
        self.data_path = os.path.join(data_dir, "movie_data.csv")
        # Vectorizer import library for text to numbers
        self.vectorizer = TfidfVectorizer(max_features=1000)
        # Forest model creation
        self.model = RandomForestRegressor(n_estimators=100)
        
    def train_model(self):
        """Training the model with our movie data"""
        # CSV into a dataframe
        df = pd.read_csv(self.data_path)
        
        # Filtering for output summary, truncation 
        df = df[(df['movie_summary'].str.len() > 50) & 
                (df['movie_rating'].between(0, 10))]
        
        # Vector needs an array
        X = self.vectorizer.fit_transform(df['movie_summary'])
        # Get the movie rating
        y = df['movie_rating']
        
        # Train for model
        self.model.fit(X, y)
        
        # Save model
        joblib.dump(self.vectorizer, 'text_processor.joblib') #if these files ares present run test file again
        joblib.dump(self.model, 'rating_predictor.joblib')
        print("Model training complete!")
    
    def predict_rating(self, plot_text):
        """Predict a movie rating from a plot text"""
        # Load the saved vectorizer and model
        vectorizer = joblib.load('text_processor.joblib')
        model = joblib.load('rating_predictor.joblib')
        # Convert the new plot text into a number array
        X = vectorizer.transform([plot_text])
        # Predict the rating and round it to 1 decimal place
        return round(model.predict(X)[0], 1)
