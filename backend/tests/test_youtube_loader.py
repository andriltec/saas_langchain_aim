import requests
import json

def test_youtube_transcript():
    # URL do endpoint
    url = "http://localhost:8000/youtube/transcript"
    
    # Dados da requisição seguindo exatamente a documentação
    payload = {
        "youtube_url": "https://www.youtube.com/watch?v=QsYGlZkevEg",
        "add_video_info": False,
        "language": ["en"],
        "translation": None,
        "transcript_format": None,
        "chunk_size_seconds": 120
    }
    
    try:
        # Faz a requisição POST
        print("\nEnviando requisição para:", url)
        print("Payload:", json.dumps(payload, indent=2))
        
        response = requests.post(url, json=payload)
        
        # Imprime o status code e headers
        print("\nStatus Code:", response.status_code)
        print("Headers:", dict(response.headers))
        
        # Se houver erro, mostra os detalhes
        if response.status_code >= 400:
            try:
                error_data = response.json()
                print("\nErro detalhado:", json.dumps(error_data, indent=2))
            except:
                print("\nConteúdo da resposta de erro:", response.text)
            return
        
        # Obtém os dados da resposta
        data = response.json()
        
        # Imprime o resultado formatado
        print("\nResposta da API:")
        print("Status:", data.get("status"))
        
        if data.get("status") == "success":
            result = data.get("data", [])
            if isinstance(result, list):
                print(f"\nNúmero de chunks: {len(result)}")
                # Mostra o primeiro chunk como exemplo
                if result:
                    print("\nPrimeiro chunk:")
                    print(json.dumps(result[0], indent=2))
            else:
                print("\nConteúdo da transcrição:")
                print(json.dumps(result, indent=2))
        else:
            print("Erro:", data.get("message"))
            
    except requests.exceptions.RequestException as e:
        print(f"Erro na requisição: {e}")
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

def test_youtube_transcript_with_chunks():
    # URL do endpoint
    url = "http://localhost:8000/youtube/transcript"
    
    # Dados da requisição para teste com chunks (usando o mesmo vídeo)
    payload = {
        "youtube_url": "https://www.youtube.com/watch?v=QsYGlZkevEg",
        "add_video_info": True,
        "language": ["en"],
        "translation": None,
        "transcript_format": "CHUNKS",
        "chunk_size_seconds": 30
    }
    
    try:
        print("\nTestando transcrição com chunks...")
        print("Payload:", json.dumps(payload, indent=2))
        
        response = requests.post(url, json=payload)
        
        print("\nStatus Code:", response.status_code)
        print("Headers:", dict(response.headers))
        
        if response.status_code >= 400:
            try:
                error_data = response.json()
                print("\nErro:", json.dumps(error_data, indent=2))
            except:
                print("\nConteúdo da resposta de erro:", response.text)
            return
            
        data = response.json()
        if data.get("status") == "success":
            result = data.get("data", [])
            print(f"\nNúmero de chunks obtidos: {len(result) if isinstance(result, list) else 1}")
            if result and isinstance(result, list) and len(result) > 0:
                print("\nPrimeiro chunk:")
                print(json.dumps(result[0], indent=2))
        else:
            print("\nErro:", data.get("message"))
            
    except Exception as e:
        print(f"Erro no teste com chunks: {e}")

if __name__ == "__main__":
    print("Iniciando teste do YouTube Loader...")
    print("\n1. Teste básico de transcrição:")
    test_youtube_transcript()
    
    print("\n2. Teste de transcrição com chunks:")
    test_youtube_transcript_with_chunks()
