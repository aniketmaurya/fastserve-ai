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

### Serve SSD-1B

```python
from fastserve.models import FastServeSSD

serve = FastServeSSD(device="cuda")
serve.run_server()
```

or, run `python -m fastserve.models --model ssd-1b` from terminal.


<!-- ## Demo

Insert gif or link to demo -->


<!-- ## FAQ

#### Question 1

Answer 1

#### Question 2

Answer 2 -->