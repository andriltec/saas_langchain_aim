from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from langchain_community.document_loaders import YoutubeLoader
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound
import re

class YouTubeTranscriptRequest(BaseModel):
    youtube_url: str
    add_video_info: bool = False
    language: List[str] = ["en"]
    translation: Optional[str] = None
    transcript_format: Optional[str] = None
    chunk_size_seconds: Optional[int] = None

class YouTubeTranscriptLoader:
    def __init__(self, request: YouTubeTranscriptRequest):
        self.request = request
        self.video_id = self._extract_video_id(request.youtube_url)
        
    def _extract_video_id(self, url: str) -> str:
        """Extrai o ID do vídeo da URL do YouTube."""
        patterns = [
            r'(?:v=|\/videos\/|embed\/|youtu.be\/|\/v\/|\/e\/|watch\?v%3D|watch\?feature=player_embedded&v=|%2Fvideos%2F|embed%\u200C\u200B2F|youtu.be%2F|%2Fv%2F)([^#\&\?\n]*)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
                
        raise ValueError("URL do YouTube inválida")

    def _get_video_info(self) -> Dict[str, Any]:
        """Tenta obter informações do vídeo, retorna dicionário vazio se falhar."""
        try:
            loader = YoutubeLoader.from_youtube_url(
                self.request.youtube_url,
                add_video_info=True
            )
            docs = loader.load()
            if docs:
                return {
                    "title": docs[0].metadata.get("title", ""),
                    "description": docs[0].metadata.get("description", ""),
                    "view_count": docs[0].metadata.get("view_count", 0),
                    "author": docs[0].metadata.get("author", ""),
                    "length": docs[0].metadata.get("length", 0),
                }
        except Exception as e:
            print(f"Erro ao obter informações do vídeo: {e}")
        return {}

    def load(self) -> Dict[str, Any]:
        """Carrega a transcrição do vídeo do YouTube."""
        try:
            # Verifica se o vídeo tem legendas disponíveis
            transcript_list = YouTubeTranscriptApi.list_transcripts(self.video_id)
            
            # Tenta obter a transcrição na língua preferida
            transcript = None
            for lang in self.request.language:
                try:
                    if self.request.translation:
                        transcript = transcript_list.find_transcript(self.request.language).translate(self.request.translation)
                    else:
                        transcript = transcript_list.find_transcript([lang])
                    break
                except NoTranscriptFound:
                    continue
            
            if transcript is None:
                # Se não encontrou nas línguas preferidas, tenta pegar qualquer transcrição disponível
                transcript = transcript_list.find_transcript(transcript_list.transcript_data[0]["language_code"])
            
            # Obtém a transcrição
            transcript_data = transcript.fetch()
            
            # Se precisar adicionar informações do vídeo
            video_info = {}
            if self.request.add_video_info:
                video_info = self._get_video_info()
            
            # Processa a transcrição de acordo com o formato solicitado
            if self.request.transcript_format == "CHUNKS" and self.request.chunk_size_seconds:
                chunks = self._create_chunks(transcript_data, self.request.chunk_size_seconds)
                result = []
                for chunk in chunks:
                    chunk_data = {
                        "text": chunk["text"],
                        "start": chunk["start"],
                        "duration": chunk["duration"]
                    }
                    if video_info:
                        chunk_data["video_info"] = video_info
                    result.append(chunk_data)
                return {"status": "success", "data": result}
            else:
                # Formato padrão: texto completo
                full_text = " ".join(item["text"] for item in transcript_data)
                result = {"text": full_text}
                if video_info:
                    result["video_info"] = video_info
                return {"status": "success", "data": result}
                
        except TranscriptsDisabled:
            return {"status": "error", "message": "As legendas estão desativadas para este vídeo"}
        except NoTranscriptFound:
            return {"status": "error", "message": "Nenhuma legenda encontrada para este vídeo"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def _create_chunks(self, transcript: List[Dict], chunk_size_seconds: int) -> List[Dict]:
        """Cria chunks da transcrição baseado no tamanho em segundos."""
        chunks = []
        current_chunk = {"text": "", "start": 0, "duration": 0}
        chunk_start_time = 0
        
        for item in transcript:
            if current_chunk["duration"] >= chunk_size_seconds:
                chunks.append(current_chunk)
                chunk_start_time = item["start"]
                current_chunk = {"text": "", "start": chunk_start_time, "duration": 0}
            
            if current_chunk["text"]:
                current_chunk["text"] += " "
            current_chunk["text"] += item["text"]
            current_chunk["duration"] = item["start"] + item["duration"] - chunk_start_time
        
        if current_chunk["text"]:
            chunks.append(current_chunk)
        
        return chunks
