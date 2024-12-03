from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from loaders.youtube_loader import YouTubeTranscriptLoader, YouTubeTranscriptRequest

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React app's address
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class InputData(BaseModel):
    text: str

@app.get("/")
async def root():
    return {"message": "LangChain API is running"}

@app.post("/process")
async def process_data(data: InputData):
    # Here we'll implement LangChain processing later
    return {"result": f"Processed: {data.text}"}

@app.post("/youtube/transcript")
async def get_youtube_transcript(request: YouTubeTranscriptRequest):
    """
    Endpoint para obter a transcrição de um vídeo do YouTube.
    
    Args:
        request (YouTubeTranscriptRequest): Parâmetros da requisição
        
    Returns:
        dict: Transcrição do vídeo e metadados
    """
    loader = YouTubeTranscriptLoader(request)
    result = loader.load()
    
    if result["status"] == "error":
        raise HTTPException(status_code=400, detail=result["message"])
        
    return result
