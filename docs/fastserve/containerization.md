# Run and deploy with Docker container 🐳

## Containerization

To containerize your FastServe application, a Docker example is provided in the [examples/docker-compose-example](https://github.com/gradsflow/fastserve-ai/tree/main/examples/docker-compose-example) directory. The example is about face recognition and includes a `Dockerfile` for creating a Docker image and a `docker-compose.yml` for easy deployment. Here's a quick overview:

- **Dockerfile**: Defines the environment, installs dependencies from `requirements.txt`, and specifies the command to run your FastServe application.
- **docker-compose.yml**: Simplifies the deployment of your FastServe application by defining services, networks, and volumes.

To use the example, navigate to the `examples/docker-compose-example` directory and run:

```shell
docker-compose up --build
```

This will build the Docker image and start your FastServe application in a container, making it accessible on the specified port.

> **Note:** We provide an example using face recognition. If you need to use other models, you will likely need to change the requirements.txt or the Dockerfile. Don't worry; this example is intended to serve as a quick start. Feel free to modify it as needed.

## Passing Arguments to Uvicorn in `run_server()`
FastServe leverages Uvicorn, a lightning-fast ASGI server, to serve machine learning models, making FastServe highly efficient and scalable.
The `run_server()` method supports passing additional arguments to uvicorn by utilizing `*args` and `**kwargs`. This feature allows you to customize the server's behavior without modifying the source code. For example:

```shell
app.run_server(host='0.0.0.0', port=8000, log_level='info')
```

In this example, host, port, and log_level are passed directly to uvicorn.run() to specify the server's IP address, port, and logging level. You can pass any argument supported by `uvicorn.run()` to `run_server()` in this manner.
