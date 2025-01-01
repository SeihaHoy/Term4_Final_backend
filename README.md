# Project Term4_Final

## Running the Project via Docker

To run this project using Docker, follow the steps below:

### Prerequisites

- Ensure you have Docker installed on your machine. You can download it from [here](https://www.docker.com/products/docker-desktop).

### Steps

1. **Clone the Repository**

    ```sh
    git clone https://github.com/yourusername/Term4_Final.git
    cd Term4_Final
    ```

2. **Build the Docker Image**

    ```sh
    docker build -t term4_final_image .
    ```

3. **Run the Docker Container**

    ```sh
    docker run -d -p 8000:8000 --name term4_final_container term4_final_image
    ```

4. **Access the Application**

    Open your web browser and go to `http://localhost:8000` to access the application.

### Stopping the Container

To stop the running container, use the following command:

```sh
docker stop term4_final_container
```

### Removing the Container

To remove the container, use the following command:

```sh
docker rm term4_final_container
```

### Additional Information

- If you need to rebuild the image, use the `--no-cache` option:

  ```sh
  docker build --no-cache -t term4_final_image .
  ```

- To view the logs of the running container:

  ```sh
  docker logs term4_final_container
  ```

- To access the container's shell:

  ```sh
  docker exec -it term4_final_container /bin/bash
  ```

