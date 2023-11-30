import argparse

from fastserve.utils import get_default_device

from .ssd import FastServeSSD

parser = argparse.ArgumentParser(description="Serve models with FastServe")
parser.add_argument("--model", type=str, required=True, help="Name of the model")
parser.add_argument("--device", type=str, required=False, help="Device")


args = parser.parse_args()

app = None
device = args.device or get_default_device()

if args.model == "ssd-1b":
    app = FastServeSSD(device=device)
else:
    raise Exception(f"FastServe.models doesn't implement model={args.model}")

app.run_server()
