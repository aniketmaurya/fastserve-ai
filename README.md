# FastServe

Machine Learning Serving focused on LLMs with simplicity as the top priority.

## Installation

```bash
git clone https://github.com/aniketmaurya/fastserve.git
cd fastserve
pip install .
```

## Run locally

```bash
python -m fastserve
```

## Usage/Examples

### Serve Mistral-7B with Llama-cpp

```python
from fastserve.models import ServeLlamaCpp

model_path = "openhermes-2-mistral-7b.Q5_K_M.gguf"
serve = ServeLlamaCpp(model_path=model_path,)
serve.run_server()
```

or, run `python -m fastserve.models --model llama-cpp --model_path openhermes-2-mistral-7b.Q5_K_M.gguf` from terminal.


### Serve SDXL Turbo

```python
from fastserve.models import ServeSSD1B

serve = ServeSSD1B(device="cuda", batch_size=2, timeout=1)
serve.run_server()
```

or, run `python -m fastserve.models --model sdxl-turbo --batch_size 2 --timeout 1` from terminal.


<!-- ## Demo

Insert gif or link to demo -->


<!-- ## FAQ

#### Question 1

Answer 1

#### Question 2

Answer 2 -->