from pydantic import BaseModel

class Input_For_Post_And_Put(BaseModel):
    codename : str
    password : str
    description : str
