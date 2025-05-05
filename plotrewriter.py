from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import torch

#
class PlotRewriter:
    def __init__(self):
        # forcing gpu usage, system dependant. If using laptop with no gpu it should default to cpu
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        # Using Mistral, runs better than others i tried. Needs a lot of VRAM
        self.model_name = "teknium/OpenHermes-2.5-Mistral-7B"
        
        # Troubleshoot for tokenizer issue
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        # mappign gpu device, float 16 works better on my memory, and forcing 4bit for low vram
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            device_map="auto",           
            torch_dtype=torch.float16,   
            load_in_4bit=True            
        )
        
    def generate_alternative_summary(self, original_summary, rating, tone="neutral"):
        # Prompt for model
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
        
        # Removing "assistant" labels and "system" labels to clean up output
        new_summary = full_response.split("assistant")[-1].strip()
        return new_summary

                
        