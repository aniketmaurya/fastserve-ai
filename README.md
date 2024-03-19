<p align="center">
  <img width="250" alt="logo" src="https://ik.imagekit.io/gradsflow/logo/v2/Gradsflow-gradient_TPwd2H3s4.png?updatedAt=1710283252606"/>
  <br>
  <strong>Machine Learning Serving focused on GenAI & LLMs with simplicity as the top priority.</strong>
</p>
<p align="center">
  <a href="https://fastserve.gradsflow.com">Docs</a> |
  <a href="https://github.com/gradsflow/fastserve-ai/tree/main/examples">Examples</a>
</p>

---


## Installation

**Stable:**
```shell
pip install FastServeAI
```

**Latest:**
```shell
pip install git+https://github.com/gradsflow/fastserve-ai.git@main
```


## Usage/Examples

<a href="https://www.youtube.com/watch?v=GfcmyfPB9qY">
    <img src="https://img.youtube.com/vi/GfcmyfPB9qY/0.jpg" width=350px>
</a>

> YouTube: How to serve your own GPT like LLM in 1 minute with FastServe.



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


## Contribute

**Install in editable mode:**

```shell
git clone https://github.com/gradsflow/fastserve-ai.git
cd fastserve
pip install -e .
```

**Create a new branch**

```shell
git checkout -b ＜new-branch＞
```

**Make your changes, commit and [create a PR](https://github.com/gradsflow/fastserve-ai/compare).**


<!-- ## FAQ

#### Question 1

Answer 1

#### Question 2

Answer 2 -->
