
from fastapi import FastAPI

# routers ------------------------------
from app.users.router import router as users_router



app = FastAPI() 

# plug routers: 
app.include_router(users_router)


# TEST 
@app.get('/test')
async def app_test():
    return {'message':'Hello from app'}

