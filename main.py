from typing import List
from uuid import uuid4
from fastapi import FastAPI, HTTPException
from models import User, UserUpdateRequest, Gender, Role, UUID

app = FastAPI()

db: List[User] = [
    User(
        id=uuid4(), 
        first_name='Jamila', 
        last_name="Leon", 
        gender= Gender.female,
        roles= [Role.student]
        ),
    User(
        id=uuid4(), 
        first_name='Alex', 
        last_name="Rodriguez", 
        middle_name="Nieto",
        gender= Gender.male,
        roles= [Role.admin, Role.user]
        ),
]


@app.get('/')
def root():
    return {
        "Hello": "Mundo"
    }

@app.get('/api/v1/users')
async def fetch_users():
    return db

@app.post('/api/v1/users')
async def register_user(user: User):
    db.append(user)
    return {"id": user.id}

@app.delete('/api/v1/users/{user_id}')
async def delete_user(user_id: UUID):
    for user in db:
        if user.id == user_id:
            db.remove(user)
            return {"message": "User deleted successfully"}
    raise HTTPException (
        status_code=404,
        detail=f'user with id: {user_id} does not exist'
    )

@app.put('/api/v1/users/{id}')
async def update_user(id: UUID, updated_user: UserUpdateRequest):
    for user in db:
        if user.id == id:
            if updated_user.first_name is not None:
                user.first_name = updated_user.first_name
            if updated_user.last_name is not None:
                user.last_name = updated_user.last_name
            if updated_user.middle_name is not None:
                user.middle_name = updated_user.middle_name
            if updated_user.roles is not None:
                user.roles = updated_user.roles
            return {"message": "User updated successfully"}
    raise HTTPException (
        status_code=404,
        detail=f'user with id: {id} does not exist'
    )
