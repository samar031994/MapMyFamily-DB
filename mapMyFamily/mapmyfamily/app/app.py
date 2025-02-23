import json
from fastapi.responses import Response
from fastapi import FastAPI, Body, HTTPException, status
from pydantic.functional_validators import BeforeValidator
from fastapi import status
from typing_extensions import Annotated
from pydantic import BaseModel, EmailStr, Field
#from .model.tree_diagram import TreeDiagram, User
from bson import ObjectId
import motor.motor_asyncio
from pymongo import ReturnDocument
import os
from typing import Optional

app = FastAPI(
    title="FastAPI MongoDB API for MapMyFamily",
    summary="API backend for MapMyFamily using MongoDB.",
)

client = motor.motor_asyncio.AsyncIOMotorClient('mongodb+srv://mapmyfamily:qwerty1234@mapmyfamily.kqzwp.mongodb.net/?retryWrites=true&w=majority&appName=MapMyFamily')
db = client.map_my_family
user_collection = db.get_collection("User")
tree_diagram_collection = db.get_collection("TreeDiagram")
PyObjectId = Annotated[str, BeforeValidator(str)]

class TreeDiagram(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    model_data: dict
    users: list[str]

class User(BaseModel):
    """
    Container for a single user record.
    """
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    name: str = Field(...)
    email: EmailStr = Field(...)
    user_id: str = Field(...)

@app.post(
    "/user/",
    response_description="Add new user",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_user(user: User = Body(...)):
    """
    Insert a new student record.

    A unique `id` will be created and provided in the response.
    """
    new_user = await user_collection.insert_one(
        user.model_dump(by_alias=True, exclude=["id"])
    )
    return new_user

@app.get(
    "/user/{user_id}",
    response_description="Get user by user_id",
    response_model=User,
    status_code=status.HTTP_200_OK,
    response_model_by_alias=False,
)
async def fetch_user(user_id: str):
    user = await user_collection.find_one({"user_id": user_id})
    return user

@app.post(
    '/tree_diagram/',
    response_description="Add new tree diagram",
    response_model=TreeDiagram,
    status_code=status.HTTP_201_CREATED,
)
async def create_tree_diagram(tree_diagram: TreeDiagram = Body(...)):
    """
    Insert a new tree diagram record.

    A unique `id` will be created and provided in the response.
    """
    new_tree_diagram = await tree_diagram_collection.insert_one(
        tree_diagram.model_dump(by_alias=True, exclude=["id"])
    )
    created_tree_diagram = await tree_diagram_collection.find_one(
        {"_id": new_tree_diagram.inserted_id}
    )
    return created_tree_diagram

@app.get(
    '/tree_diagram/{tree_diagram_id}',
    response_description="Get tree diagram by tree_diagram_id",
    response_model=TreeDiagram,
)
async def fetch_tree_diagram(tree_diagram_id: str):
    tree_diagram = await tree_diagram_collection.find_one({"_id": ObjectId(tree_diagram_id)})
    return tree_diagram 

@app.options(
    "/tree_diagram/",
    response_description="Get all tree diagrams",
)
async def create_tree_options():
    content = {"message": "Options response"}
    headers = {
        "Access-Control-Allow-Origin" : "http://localhost:3000",
        "Access-Control-Allow-Credentials" : "true",
        "Access-Control-Allow-Methods" : "GET, POST, OPTIONS",
        "Access-Control-Allow-Headers" : "Content-Type, Origin, Accept"
        }
    return Response(content=json.dumps(content), headers=headers)
    