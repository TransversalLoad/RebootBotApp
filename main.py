from data_preparation import DataLoader
from plotrewriter import PlotRewriter
from rating_predictor import RatingPredictor
import gradio as gr
import os

# TMain bot class
class RebootBot:
  def __init__(self, data_dir):
    # Init and load stuff
    self.data_loader = DataLoader(data_dir)  # loading data folde
    self.plot_rewriter = PlotRewriter()        # load plot module
    self.rating_predictor = RatingPredictor(data_dir)  # load the rating predictor
    self.movie_data = self.data_loader.load_data()  # getting the movie data

  def get_movie_list(self):
    # retrieve movie names from data foldr
    return self.data_loader.get_movie_list()

  def get_summary(self, movie_name, tone):
    # Find movie from name
    movie = self.movie_data[self.movie_data["movie_name"] == movie_name].iloc[0]
    original = movie["movie_summary"]  # original summary getter
    # rewriting function for BotReboot
    rewritten = self.plot_rewriter.generate_alternative_summary(
      original, 
      movie["movie_rating"],
      tone
    )
    return original, rewritten

  def predict_plot_rating(self, plot_text):
    # Predict a rating for user input plot
    return self.rating_predictor.predict_rating(plot_text)


def create_interface():
  # This is my dataset path, replace this with your RebootBot\Movies path shivang 
  dataset_path = r"C:\Users\wkacc\Documents\University\SWE Y4\Shivang\Assignment 1\RebootBot\Datasets\Movies"
  
  # Make bot 
  bot = RebootBot(dataset_path)
  
  # Implementing gradio
  with gr.Blocks() as interface:
    gr.Markdown("# 🍿 RebootBot - Movie Magic Machine")

    #dropdowns for movie and tone selection
    with gr.Tab("🔄 Rewrite Plots"):
      gr.Markdown("**Change the tone of movie summaries**")
      movie_dd = gr.Dropdown(bot.get_movie_list(), label="Select Movie")
      tone_dd = gr.Dropdown(["neutral", "funny", "horror", "dramatic"], label="Tone")
      rewrite_btn = gr.Button("Rewrite", variant="primary")
      
      #output boxes 
      with gr.Row():
        original_tb = gr.Textbox(label="Original Summary", lines=5)
        rewritten_tb = gr.Textbox(label="New Version", lines=5)
    
    with gr.Tab("Predict Ratings!"):
      gr.Markdown("**How good is your plot according to IMBd?**")
      plot_input = gr.Textbox(label="Enter Plot", lines=3)
      predict_btn = gr.Button("Predict", variant="primary")
      rating_out = gr.Number(label="Predicted Rating (0-10)", precision=1)
    
    # Hook up the buttons to our functions using lambda functions
    rewrite_btn.click(fn=lambda m, t: bot.get_summary(m, t),
                      inputs=[movie_dd, tone_dd],
                      outputs=[original_tb, rewritten_tb])
    
    predict_btn.click(fn=lambda t: bot.predict_plot_rating(t),
                      inputs=plot_input,
                      outputs=rating_out)
    
  return interface


if __name__ == "__main__":
  # For first time setup, not sure if youll need this shivang: 
  #if you dont have 2 joblib files on the left here <-- uncomment the below line, insert dataset path
  # path = RebootBot\Movies" and run main.py once. then re comment
  # RatingPredictor(r"C:\Users\wkacc\Documents\University\SWE Y4\Shivang\Assignment 1\RebootBot\Datasets\Movies").train_model()
  
  inter = create_interface()  # creates the interface
  inter.launch()  # runs 
