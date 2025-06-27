from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from models.input import Input_For_Post_And_Put
from db import collection

app = FastAPI(
    title="Agent Management API",
    description="A CRUD API for managing agents with MongoDB",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "agents",
            "description": "Operations with agents",
        }
    ]
)

@app.get("/agent/{codename}/{password}", status_code=200, tags=["agents"])
def getAgent(codename : str,password:str):
    """
    Get an agent by codename and password
    
    - **codename**: The agent's codename
    - **password**: The agent's password
    """
    agent = collection.find_one({"codename": codename, 'password':password})
    if agent:
        agent["_id"] = str(agent["_id"])
        return agent
    else:
        raise HTTPException(status_code=404, detail="Agent not found")

@app.post("/agent/", status_code=201, tags=["agents"])
def createAgent(details : Input_For_Post_And_Put):
    """
    Create a new agent
    
    - **codename**: Unique codename for the agent
    - **password**: Password for the agent
    - **description**: Description of the agent
    """
    try :
        agent = collection.find_one({"codename": dict(details)['codename']})
        if agent :
            raise HTTPException(status_code=409, detail="Agent with this codename already exists.")
        response = collection.insert_one(dict(details))
        return {"id" : str(response.inserted_id)}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"ERROR OCCURED {e}")
    
@app.delete("/agent/{codename}/{password}", status_code=200, tags=["agents"])
def deleteAgent(codename: str, password: str):
    """
    Delete an agent by codename and password
    
    - **codename**: The agent's codename
    - **password**: The agent's password
    """
    result = collection.delete_one({"codename": codename, "password": password})
    if result.deleted_count == 1:
        return {"detail": "Agent deleted successfully."}
    else:
        raise HTTPException(status_code=404, detail="Agent not found or password incorrect.")

@app.put("/agent/", status_code=200, tags=["agents"])
def updateAgent(details : Input_For_Post_And_Put):
    """
    Update an existing agent
    
    - **codename**: The agent's codename (used for identification)
    - **password**: The agent's current password (used for identification)
    - **description**: New description for the agent
    """
    update_data = dict(details)
    result = collection.update_one(
        {"codename": update_data['codename'], "password": update_data['password']},
        {"$set": update_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Agent not found or password incorrect.")
    return {"detail": "Agent updated successfully."}