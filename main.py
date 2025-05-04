from data_preparation import DataLoader
from plotrewriter import PlotRewriter
import gradio as gr
import os

# defining our rebootclass 
class RebootBot:
    def __init__(self, data_dir):
        self.data_dir = data_dir
        self.data_loader = DataLoader(data_dir)
        self.plot_rewriter = PlotRewriter()
        self.df = self.data_loader.load_and_merge_data()
        self.movie_list = self.data_loader.get_movie_list()
        
    def get_summary(self, movie_name, tone):
        movie_data = self.df[self.df["movie_name"] == movie_name].iloc[0]
        original = movie_data["movie_summary"]
        rewritten = self.plot_rewriter.generate_alternative_summary(
            original, 
            movie_data["movie_rating"],
            tone
        )
        return original, rewritten

# Then defining the interface functions
def create_interface():
    dataset_path = r"C:\Users\wkacc\Documents\University\SWE Y4\Shivang\Assignment 1\RebootBot\Datasets\Movies"
    
    #error check for missing dataset
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Dataset directory not found: {dataset_path}")
    
    bot = RebootBot(data_dir=dataset_path)
    return gr.Interface(
        fn=lambda movie,tone: bot.get_summary(movie, tone),
        inputs=[
            gr.Dropdown(bot.movie_list, label="Select Movie"),
            gr.Dropdown(["neutral", "humorous", "dramatic", "horror", "thrilling"], label="Tone")
        ],
        outputs=[
            gr.Textbox(label="Original Summary"),
            gr.Textbox(label="RebootBot Version")
        ],
        title="🎬 RebootBot - Movie Summary Rewriter",
        description="Create alternative versions of movie plots!"
    )

# Main execution at the END
if __name__ == "__main__":
    interface = create_interface()
    interface.launch()