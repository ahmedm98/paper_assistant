from fastapi import FastAPI
from pydantic import BaseModel
from utils import Similarity_calculator

class User_input(BaseModel):
    '''Represents the user input.

    :param paragraph: user text input.
    :type paragraph: str
    :param k: the number of papers to be suggested.
    :type k: int
    '''
    paragraph : str
    k : int


app = FastAPI()
sim_calc = Similarity_calculator()

@app.post("/get_papers")
def get_papers(input:User_input):
    result = sim_calc.get_top(input.paragraph,input.k)
    return result