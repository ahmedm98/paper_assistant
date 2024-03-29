# Paper Assistant
This repository hosts the code for the Paper Assistant Web Application, a dynamic tool designed for researchers and academics. It allows users to build and manage a personalized database of research papers in PDF format. The application is equipped with several features, including paper summarization, Retrieval-Augmented Generation (RAG) for enhanced information processing, and a search functionality to navigate through your collection of research documents efficiently. This user-friendly platform is ideal for streamlining research activities and accessing key information swiftly.

#   Setup
To get the Paper Assistant Web Application up and running, follow these setup instructions:

### 1. Hosting a GROBID Server ###  

- Host a [GROBID server](https://grobid.readthedocs.io/en/latest/Run-Grobid/) by running a docker container. This can be done either locally on your machine or on a cloud platform.
- After setting up the server, enter the server's IP address in the grobid_config.json file located in the backend/configs/ directory.

### 2. Configure OpenAI's Key ###

- Obtain an API key from [OpenAI](https://platform.openai.com/docs/api-reference/authentication)
- Place your OPENAI_KEY in a .env file in the backend folder.

### 3. Running the Application

- Make sure your [docker](https://www.docker.com/products/docker-desktop/) daemon is running.
- In the root folder, run
```
docker compose up
```

