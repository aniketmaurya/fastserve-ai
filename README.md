# FastServe

Machine Learning Serving focused on GenAI & LLMs with simplicity as the top priority.

> [![img_tag](https://img.youtube.com/vi/GfcmyfPB9qY/0.jpg)](https://www.youtube.com/watch?v=GfcmyfPB9qY)
>
> YouTube: How to serve your own GPT like LLM in 1 minute with FastServe

## Installation

**Stable:**
```shell
pip install FastServeAI
```

**Latest:**
```shell
pip install git+https://github.com/aniketmaurya/fastserve.git@main
```

## Run locally

```bash
python -m fastserve
```

## Usage/Examples


### Serve LLMs with Llama-cpp

```python
from fastserve.models import ServeLlamaCpp

model_path = "openhermes-2-mistral-7b.Q5_K_M.gguf"
serve = ServeLlamaCpp(model_path=model_path, )
serve.run_server()
```

or, run `python -m fastserve.models --model llama-cpp --model_path openhermes-2-mistral-7b.Q5_K_M.gguf` from terminal.


### Serve vLLM

```python
from fastserve.models import ServeVLLM

app = ServeVLLM("TinyLlama/TinyLlama-1.1B-Chat-v1.0")
app.run_server()
```

You can use the FastServe client that will automatically apply chat template for you -

```python
from fastserve.client import vLLMClient
from rich import print

client = vLLMClient("TinyLlama/TinyLlama-1.1B-Chat-v1.0")
response = client.chat("Write a python function to resize image to 224x224", keep_context=True)
# print(client.context)
print(response["outputs"][0]["text"])
```


### Serve SDXL Turbo

```python
from fastserve.models import ServeSDXLTurbo

serve = ServeSDXLTurbo(device="cuda", batch_size=2, timeout=1)
serve.run_server()
```

or, run `python -m fastserve.models --model sdxl-turbo --batch_size 2 --timeout 1` from terminal.

This application comes with an UI. You can access it at [http://localhost:8000/ui](http://localhost:8000/ui) .


<img src="https://raw.githubusercontent.com/aniketmaurya/fastserve/main/assets/sdxl.jpg" width=400 style="border: 1px solid #F2F3F5;">


### Face  Detection

```python
from fastserve.models import FaceDetection

serve = FaceDetection(batch_size=2, timeout=1)
serve.run_server()
```

or, run `python -m fastserve.models --model face-detection --batch_size 2 --timeout 1` from terminal.

### Image Classification

```python
from fastserve.models import ServeImageClassification

app = ServeImageClassification("resnet18", timeout=1, batch_size=4)
app.run_server()
```

or, run `python -m fastserve.models --model image-classification --model_name resnet18 --batch_size 4 --timeout 1` from
terminal.

### Serve HuggingFace Models

You can easily serve any HuggingFace Transformer model using FastServe.

For some models, it is required to have a HuggingFace API token correctly set up in your environment to access models from the HuggingFace Hub.
This is not necessary for all models, but you may encounter this requirement, such as accepting terms of use or any other necessary steps. Take a look at your model's page for specific requirements.
```
export HUGGINGFACE_TOKEN=<your hf token>
```

Example of run the server:
```python
from fastserve.models import ServeHuggingFace

# Here, we use "gpt2" as an example. Replace "gpt2" with the name of your desired model.
# The `model_name` parameter is optional; the class can retrieve it from an environment variable called `HUGGINGFACE_MODEL_NAME`.
app = ServeHuggingFace(model_name="gpt2") 
app.run_server()
```

or, run `python -m fastserve.models --model huggingface --model_name bigcode/starcoder --batch_size 4 --timeout 1` from
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


### Serve Custom Model

To serve a custom model, you will have to implement `handle` method for `FastServe` that processes a batch of inputs and
returns the response as a list.

```python
from fastserve import FastServe


class MyModelServing(FastServe):
    def __init__(self):
        super().__init__(batch_size=2, timeout=0.1)
        self.model = create_model(...)

    def handle(self, batch: List[BaseRequest]) -> List[float]:
        inputs = [b.request for b in batch]
        response = self.model(inputs)
        return response


app = MyModelServing()
app.run_server()
```

You can run the above script in terminal, and it will launch a FastAPI server for your custom model.

## Deploy

### Lightning AI Studio ⚡️

```shell
python fastserve.deploy.lightning --filename main.py \
    --user LIGHTNING_USERNAME \
    --teamspace LIGHTNING_TEAMSPACE \
    --machine "CPU"  # T4, A10G or A10G_X_4
```

## Containerization

To containerize your FastServe application, a Docker example is provided in the `examples/docker-compose-example` directory. The example is about face recognition and includes a `Dockerfile` for creating a Docker image and a `docker-compose.yml` for easy deployment. Here's a quick overview:

- **Dockerfile**: Defines the environment, installs dependencies from `requirements.txt`, and specifies the command to run your FastServe application.
- **docker-compose.yml**: Simplifies the deployment of your FastServe application by defining services, networks, and volumes.

To use the example, navigate to the `examples/docker-compose-example` directory and run:

```shell
docker-compose up --build
```

This will build the Docker image and start your FastServe application in a container, making it accessible on the specified port.

> **Note:** We provide an example using face recognition. If you need to use other models, you will likely need to change the requirements.txt or the Dockerfile. Don't worry; this example is intended to serve as a quick start. Feel free to modify it as needed.

## Passing Arguments to Uvicorn in `run_server()`
FastServe leverages Uvicorn, a lightning-fast ASGI server, to serve machine learning models, making FastServe highly efficient and scalable.
The `run_server()` method supports passing additional arguments to uvicorn by utilizing `*args` and `**kwargs`. This feature allows you to customize the server's behavior without modifying the source code. For example:

```shell
app.run_server(host='0.0.0.0', port=8000, log_level='info')
```

In this example, host, port, and log_level are passed directly to uvicorn.run() to specify the server's IP address, port, and logging level. You can pass any argument supported by `uvicorn.run()` to `run_server()` in this manner.

## Contribute

**Install in editable mode:**

```shell
git clone https://github.com/aniketmaurya/fastserve.git
cd fastserve
pip install -e .
```

**Create a new branch**

```shell
git checkout -b ＜new-branch＞
```

**Make your changes, commit and [create a PR](https://github.com/aniketmaurya/fastserve/compare).**


<!-- ## FAQ

#### Question 1

Answer 1

#### Question 2

Answer 2 -->
