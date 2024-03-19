# Serve Image Classification models with FastServe

# Image Classification

```python
from fastserve.models import ServeImageClassification

app = ServeImageClassification("resnet18", timeout=1, batch_size=4)
app.run_server()
```

or, run `python -m fastserve.models --model image-classification --model_name resnet18 --batch_size 4 --timeout 1` from
terminal.

