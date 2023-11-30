import argparse

from .ssd import FastServeSSD

parser = argparse.ArgumentParser(description="Serve models with FastServe")
parser.add_argument("--model", type=str, required=True, help="Name of the model")

args = parser.parse_args()

app = None
if args.model == "ssd-1b":
    app = FastServeSSD(device="mps")
else:
    raise Exception(f"FastServe.models doesn't implement model={args.model}")

app.run_server()
