# Serve Face  Detection

```python
from fastserve.models import FaceDetection

serve = FaceDetection(batch_size=2, timeout=1)
serve.run_server()
```

or, run `python -m fastserve.models --model face-detection --batch_size 2 --timeout 1` from terminal.
