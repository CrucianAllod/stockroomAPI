import uvicorn
from contextlib import asynccontextmanager
from api.routers import all_routers
from fastapi import FastAPI


from db.database import create_tables, delete_tables


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    print("База готова")
    yield
    await delete_tables()
    print("База очищена")

app = FastAPI(lifespan=lifespan)

for router in all_routers:
    app.include_router(router, prefix="/api")
    
    
if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
