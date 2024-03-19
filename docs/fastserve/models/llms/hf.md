# 🤗 Hugging Face 

## Serve HuggingFace Models

Leveraging FastServe, you can seamlessly serve any HuggingFace Transformer model, enabling flexible deployment across various computing environments, from CPU-based systems to powerful GPU and multi-GPU setups.

For some models, it is required to have a HuggingFace API token correctly set up in your environment to access models from the HuggingFace Hub.
This is not necessary for all models, but you may encounter this requirement, such as accepting terms of use or any other necessary steps. Take a look at your model's page for specific requirements.
```
export HUGGINGFACE_TOKEN=<your hf token>
```

The server can be easily initiated with a specific model. In the example below, we demonstrate using `gpt2`. You should replace `gpt2` with your model of choice. The `model_name` parameter is optional; if not provided, the class attempts to fetch the model name from an environment variable `HUGGINGFACE_MODEL_NAME`. Additionally, you can now specify whether to use GPU acceleration with the `device` parameter, which defaults to `cpu` for CPU usage.

```python
from fastserve.models import ServeHuggingFace

# Initialize with GPU support if desired by setting `device="cuda"`.
# For CPU usage, you can omit `device` or set it to `cpu`.
app = ServeHuggingFace(model_name="gpt2", device="cuda")
app.run_server()
```

or, run `python -m fastserve.models --model huggingface --model_name bigcode/starcoder --batch_size 4 --timeout 1 --device cuda` from
terminal.

To make a request to the server, send a JSON payload with the prompt you want the model to generate text for. Here's an example using requests in Python:
```python
import requests

response = requests.post(
    "http://localhost:8000/endpoint",
    json={"prompt": "Once upon a time", "temperature": 0.7, "max_tokens": 100}
)
print(response.json())
```
This setup allows you to easily deploy and interact with any Transformer model from HuggingFace's model hub, providing a convenient way to integrate AI capabilities into your applications.


Remember, for deploying specific models, ensure that you have the necessary dependencies installed and the model files accessible if they are not directly available from HuggingFace's model hub.
