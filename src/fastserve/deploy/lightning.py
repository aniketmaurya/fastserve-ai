try:
    from lightning_sdk import Machine, Studio
except ModuleNotFoundError:
    Machine = None
    Studio = None


def lightning_job(
    user: str,
    teamspace: str = "default",
    command="python main.py",
    machine=Machine.CPU,
):
    # Start the studio
    s = Studio(name="fastserve", teamspace=teamspace, user=user, create_ok=True)
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
    parser.add_argument("--user", type=str, required=True, help="Lightning AI username")
    parser.add_argument(
        "--teamspace", type=str, required=True, help="Lightning AI teamspace"
    )
    parser.add_argument(
        "--machine",
        type=Machine,
        required=False,
        default="CPU",
        help="Lightning AI job plugin machine type",
    )

    args = parser.parse_args()

    command = f"python {args.filename}"
    lightning_job(
        command=command, user=args.user, teamspace=args.teamspace, machine=args.machine
    )
