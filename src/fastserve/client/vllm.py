import requests
import logging

class Client:
    def __init__(self):
        pass


class vLLMClient(Client):
    def __init__(self, model: str, base_url="http://localhost:8000/endpoint"):
        from transformers import AutoTokenizer
        super().__init__()
        self.tokenizer = AutoTokenizer.from_pretrained(model)
        self.context = []
        self.base_url = base_url
    
    def chat(self, prompt: str, keep_context=False):
        new_msg = {"role": "user", "content": prompt}
        if keep_context:
            self.context.append(new_msg)
            messages = self.context
        else:
            messages = [new_msg]
        
        logging.info(messages)
        chat = self.tokenizer.apply_chat_template(messages, tokenize=False)
        headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
        }
        data = {
            "prompt": chat,
            "temperature": 0.8,
            "top_p": 1,
            "max_tokens": 500,
            "stop": []
        }

        response = requests.post(self.base_url, headers=headers, json=data).json()
        if keep_context:
            self.context.append({"role": "assistant", "content": response["outputs"][0]["text"]})
        return response
