from transformers import pipeline
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig

class ReaderLLM:
    def __init__(self, model_name) -> None:
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_compute_dtype=torch.bfloat16,
        )
        
        self.model = AutoModelForCausalLM.from_pretrained(model_name, quantization_config=bnb_config)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)
        self.model.eval()
        self.generator = pipeline(model=self.model, 
                                tokenizer=self.tokenizer,
                                task="text-generation",
                                do_sample=True,
                                temperature=0.2,
                                repetition_penalty=1.1,
                                return_full_text=False,
                                max_new_tokens=100,
                                device=0 if torch.cuda.is_available() else -1)

    def generate_response(self, user_query):
        response = self.generator(user_query, max_length=100, do_sample=True, temperature=0.7, top_k=50, top_p=0.95)
        return response[0]['generated_text']
    
    def tokenizer(self):
        return self.tokenizer
    
if __name__ == "__main__":
    user_query = "How to create a pipeline in transformer library?"
    reader = ReaderLLM("HuggingFaceH4/zephyr-7b-beta")
    response = reader.generate_response(user_query)
    
    print(response)