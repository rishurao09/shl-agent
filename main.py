from fastapi import FastAPI
from pydantic import BaseModel
from catalog import search_assessments

app = FastAPI()

# Request body format
class Query(BaseModel):
    message: str

# Health check endpoint
@app.get("/health")
def health():
    return {"status": "ok"}

# Chat endpoint
@app.post("/chat")
def chat(query: Query):
    results = search_assessments(query.message)

    if not results:
        return {"response": "No assessments found."}

    formatted_results = []
    for r in results[:5]:
        formatted_results.append({
            "name": r.get("name", "No name"),
            "link": r.get("url") or r.get("link") or "No link available"
        })

    return {"response": formatted_results}
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all origins (for now)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)