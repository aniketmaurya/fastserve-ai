from lightning_sdk import Machine, Studio


def lightning_job(
    command="python main.py",
    machine=Machine.CPU,
):
    # Start the studio
    s = Studio(name="fastserve", teamspace="dream-team", user="aniket")
    print("starting Studio...")
    s.start()

    # Install plugin if not installed (in this case, it is already installed)
    s.install_plugin("jobs")

    jobs_plugin = s.installed_plugins["jobs"]

    jobs_plugin.run(command, name="serve", machine=machine)

    print("Stopping Studio")
    s.stop()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Deploy FastServe")
    parser.add_argument("--filename", type=str, required=True, help="Python filename")

    args = parser.parse_args()

    command = f"python {args.filename}"
    lightning_job(command=command)
