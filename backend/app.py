from fastapi import FastAPI
from pydantic import BaseModel
from main_rag import agent
from langchain_core.messages import HumanMessage, AIMessage
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS (keep as is)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request model
class Query(BaseModel):
    question: str
    history: list = []   # coming from frontend


@app.get("/")
def home():
    return {"message": "AI Logistics Assistant API is running"}


@app.post("/chat")
def chat(q: Query):

    messages = []

    # 🔁 Convert frontend history → LangChain messages
    for msg in q.history:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        elif msg["role"] == "assistant":
            messages.append(AIMessage(content=msg["content"]))

    # ➕ Add current user question
    messages.append(HumanMessage(content=q.question))

    # 🤖 Call your RAG agent
    res = agent.invoke({"messages": messages})

    # 📤 Extract answer
    answer = res["messages"][-1].text

    return {"answer": answer}