# Serve GenAI - Image Generation Models

## Serve SDXL Turbo

```python
from fastserve.models import ServeSDXLTurbo

serve = ServeSDXLTurbo(device="cuda", batch_size=2, timeout=1)
serve.run_server()
```

or, run `python -m fastserve.models --model sdxl-turbo --batch_size 2 --timeout 1` from terminal.

This application comes with an UI. You can access it at [http://localhost:8000/ui](http://localhost:8000/ui) .


<img src="https://raw.githubusercontent.com/gradsflow/fastserve-ai/main/assets/sdxl.jpg" width=400 style="border: 1px solid #F2F3F5;">
