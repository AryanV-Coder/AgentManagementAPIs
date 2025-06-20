from fastapi import FastAPI, HTTPException
from models.input import Input_For_Post_And_Put
from db import collection

app = FastAPI()

@app.get("/agent/{codename}/{password}")
def getAgent(codename : str,password:str):
    agent = collection.find_one({"codename": codename, 'password':password})
    if agent:
        agent["_id"] = str(agent["_id"])
        return agent
    else:
        raise HTTPException(status_code=404, detail="Agent not found")

@app.post("/agent/")
def createAgent(details : Input_For_Post_And_Put):
    try :
        agent = collection.find_one({"codename": dict(details)['codename']})
        if agent :
            raise HTTPException(status_code=409, detail="Agent with this codename already exists.")
        response = collection.insert_one(dict(details))
        return {"status_code" : 201 , "id" : str(response.inserted_id)}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500,detail=f"ERROR OCCURED {e}")
    
@app.delete("/agent/{codename}/{password}")
def deleteAgent(codename: str, password: str):
    result = collection.delete_one({"codename": codename, "password": password})
    if result.deleted_count == 1:
        return {"status_code": 200, "detail": "Agent deleted successfully."}
    else:
        raise HTTPException(status_code=404, detail="Agent not found or password incorrect.")

@app.put("/agent/")
def updateAgent(details : Input_For_Post_And_Put):
    update_data = dict(details)
    result = collection.update_one(
        {"codename": update_data['codename'], "password": update_data['password']},
        {"$set": update_data}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Agent not found or password incorrect.")
    return {"status_code": 200, "detail": "Agent updated successfully."}