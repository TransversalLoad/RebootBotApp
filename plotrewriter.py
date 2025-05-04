from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline, BitsAndBytesConfig
import torch

class PlotRewriter:
    def __init__(self):
        self.model_name = "teknium/OpenHermes-2.5-Mistral-7B"   #FLAN works too
        
        # Forcing 4bit to save on VRAM
        self.bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.bfloat16,  # Match compute dtype to model
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4"
        )
        
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        self.tokenizer.pad_token = self.tokenizer.eos_token  # dont think token is needed anymore but doesnt conflict
        
        #forcing GPU usage and bfloat16 rathe than float 18
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            quantization_config=self.bnb_config,
            device_map="auto",
            torch_dtype=torch.bfloat16
        )
        
        self.pipe = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer
        )

        #humorous is the default tone is only used if other tone isnt selected 
    def generate_alternative_summary(self, original_summary, rating, tone="humorous"): 
        prompt = f"""<|im_start|>system
        You are a fan-fiction movie writer. Rewrite this summary in a {tone} tone.
        The movie has a {rating}/10 rating.
        <|im_start|>user
        {original_summary[:1000]}
        <|im_start|>assistant
        """
        #prompt variables
        outputs = self.pipe(
            prompt,
            max_new_tokens=250,
            temperature=0.85,
            top_k=40,
            top_p=0.9,
            repetition_penalty=1.2,
            do_sample=True,
            pad_token_id=self.tokenizer.eos_token_id 
        )
        
        return outputs[0]['generated_text'].split("<|im_start|>assistant")[-1].strip()