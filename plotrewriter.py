from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, BitsAndBytesConfig
import torch
from detoxify import Detoxify


#
class PlotRewriter:
    def __init__(self): # attempting to remove offensive outputs 
        self.toxicity_model = Detoxify('original')

        # forcing gpu usage, system dependant. If using laptop with no gpu it should default to cpu
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        # Using Mistral, runs better than others i tried. Needs a lot of VRAM
        self.model_name = "teknium/OpenHermes-2.5-Mistral-7B"

        # fixing bytesandbits because it keeps prompting in cmd
        self.bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16
        )

        
        # Troubleshoot for tokenizer issue
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        # mappign gpu device, float 16 works better on my memory, and forcing 4bit for low vram
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            device_map="auto",     
            quantization_config=self.bnb_config,
            torch_dtype=torch.float16
                  
        )
        
    def generate_alternative_summary(self, original_summary, rating, tone="neutral"):

        # Prompt for model   (using a template soo im_start is needed and sso is assistant)
        prompt = f"""<|im_start|>system
        Rewrite this movie summary in a {tone} tone. The movie has a {rating}/10 rating.
        - Don't include labels like "Funny Version:"
        - Don't repeat the original text
        - Reply only with the rewritten movie summary
        Original: {original_summary[:1000]}
        <|im_start|>assistant
        """
        
        # Tokenization
        # Max length 1024 to avoid running out of tokens or vram
        inputs = self.tokenizer(
            prompt,
            return_tensors="pt",
            max_length=1024,
            truncation=True
        ).to(self.device)
        
        # summary generation
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=400,   # Token Limit
            temperature=0.9,      # Raise if boring output, lower for sensible output 
            do_sample=True,       # Sampling 
            pad_token_id=self.tokenizer.eos_token_id  # Not sure if needed still
        )
        
        # decode tokens to text
        full_response = self.tokenizer.decode(
            outputs[0], 
            skip_special_tokens=True
        )

        if self._is_toxic(full_response):
            return "[Content Removal] My Apologies, this content violated our safety guidelines."
        
        # removing assistant labels and system labels to clean output
        return full_response.split("assistant")[-1].strip()


    def _is_toxic(self, text, threshold=0.7):     
        results = self.toxicity_model.predict(text)
        return any(v > threshold for v in results.values())
       
        # uncommeent if toxicity is causing problems 
       #  return new_summary

                
        