# Serve LLMs at Scale with vLLM

## Serve vLLM

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