# Paper Assistant
This repository creates a web application where you input a sentence or a paragraph, then you receive suggestions of relevant scientific papers from a database.

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
To evaluate the current method, you can run the python file evaluation.py. It conducts an experiment where for every paper's abstract, the application computes the top 3 most similar papers. If the abstract's original paper appears in the top 3 recommended papers, then this counts as a correct prediction. If not, then it counts as a false prediction.


Note that the abstracts have been omitted from the text used to summarize the papers. Also, the similarity score is computed between the input paragraph and the summary of a paper. 

evaluation.py produces an accuracy measure. To execute the file, you have to download [poetry](https://python-poetry.org/docs/#installation) then run the following command.
```
poetry run python evaluation.py
```

# Method description

- Every paper's extracted text is first preprocessed by removing the abstract, tables, title lines and empty lines. This preprocessed text is then fed to Llama2 to produce a three sentence summary for every paper. 
- Using the sentence transformer model all-mpnet-base-v2, we encode each summary as a 768 dimensional vector.
- A database is then created storing the names of the papers, their summaries, their abstracts and their vectors.
- After the user inputs a paragraph through the streamlit frontend, the paragraph is sent to the FastAPI backend where it gets encoded as a 768 vector using the all-mpnet-base-v2 model. This vector is then compared to every vector in the database by computing the cosine distance. The three papers with the highest cosine distance are picked and sent back to the frontend with their names, their summaries, their abstracts and their cosine similarity score.
- The result is then shown to the user through the streamlit frontend.

# Possible next steps

- Create other methods to compute the summaries and the similarity scores. And compare the performances of the different methods.
- Add a pipeline that lets the user add more paper to the database.
- Standardize the text preprocessing pipeline.