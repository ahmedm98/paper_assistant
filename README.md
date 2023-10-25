# Paper Assistant
This repository creates a web application where you input a sentence or a paragraph, then you recieve suggestions of relevant scientific papers from a fixed database.

# Setup
To launch the application
- First, you need to install [Docker](https://www.docker.com/products/docker-desktop/) if you do not already have it.
- Make sure the docker daemon is running (open docker desktop).
- Run the following command. It might take several minutes.
```
docker compose up
```

After all containers are up and running, You can access the application here: 
http://127.0.0.1:8501

# Evaluation
To evaluate the current method, you can run the python file evaluation.py. It conducts an experiment where for every paper's abstract, we compute the top 3 most similar papers. If the abstract's original paper appears in the top 3, then this counts as a correct prediction. If not, then it counts as a false prediction.


Note that the abstracts have been omitted from the text used to summarize the papers. Also, a similarity score is computed between the input paragraph and the summary of a paper. 

evaluation.py produces an accuracy measure. To execute the file, you have to download [poetry](https://python-poetry.org/docs/#installation) then run the following command.
```
poetry run python evaluation.py
```

