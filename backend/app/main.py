

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware


from app.api import auth, upload, data

from app.db.session import Base, engine


# Ensure tables exist (for simple dev use)

Base.metadata.create_all(bind=engine)


app = FastAPI(title="Clinical Trial Backend", version="0.1.0")


app.add_middleware(

    CORSMiddleware,

    allow_origins=["*"],  # tighten later if needed

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"],
)



@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(auth.router)
app.include_router(upload.router)
app.include_router(data.router)
