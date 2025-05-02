from transformers import pipeline


class PlotRewriter:
    def __init__(self, model_name='distilgpt2', max_new_tokens=30, temperature=0.6): # keeping the text to 200charca50 tokens because output was overly long
        # Initialising the generator
        self.generator = pipeline('text-generation', model=model_name)
        self.max_new_tokens = max_new_tokens
        self.temperature = temperature

    def rewrite_plot(self, movie_name, movie_summary, rating):
        """ This application generates an alternate plot based on the movie's name, summary, and rating. """
        prompt = (
            f"Rewrite the ending of the movie '{movie_name}'.\n"
            f"Original plot summary: {movie_summary}\n\n"
            f"It received a rating of {rating}/10. "
            "Based on this rating, create a short, clear and concise summary of a revised plot."
        )
        # Generate alternate plot hopefully, based on movie name summary the rating 
        result = self.generator(
            prompt,
            max_new_tokens=self.max_new_tokens,
            temperature=self.temperature,
            num_return_sequences=1
        )
        return result[0]['generated_text']