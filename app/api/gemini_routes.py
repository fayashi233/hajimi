from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import JSONResponse, StreamingResponse
from app.utils.auth import custom_verify_password
from app.services.gemini import GeminiClient
import json

router = APIRouter(prefix="/gemini", tags=["Gemini Native"])

# 全局变量，将在 main.py 中初始化并传入
key_manager = None

def init_gemini_router(_key_manager):
    """
    Initializes the Gemini router with necessary dependencies.
    """
    global key_manager
    key_manager = _key_manager

@router.get("/v1beta/models", response_class=JSONResponse)
async def list_gemini_models(request: Request, _ = Depends(custom_verify_password)):
    """
    Get a list of available Gemini models in the native format.
    The proxy uses its internal keys to query the Gemini API.
    """
    try:
        api_key = await key_manager.get_available_key()
        if not api_key:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="No available API keys in the proxy.")
            
        models = await GeminiClient.list_models_native(api_key)
        return {"models": models}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/v1beta/models/{model}:generateContent", response_class=JSONResponse)
async def generate_content(model: str, request: Request, _ = Depends(custom_verify_password)):
    """
    Handle native non-streaming content generation requests.
    The proxy uses its internal keys to query the Gemini API.
    """
    try:
        api_key = await key_manager.get_available_key()
        if not api_key:
            raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="No available API keys in the proxy.")

        request_data = await request.json()
        client = GeminiClient(api_key=api_key)
        response_data = await client.generate_content_native(model, request_data)
        return response_data
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON in request body")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/v1beta/models/{model}:streamGenerateContent", response_class=StreamingResponse)
async def stream_generate_content(model: str, request: Request, _ = Depends(custom_verify_password)):
    """
    Handle native streaming content generation requests.
    The proxy uses its internal keys to query the Gemini API.
    """
    try:
        api_key = await key_manager.get_available_key()
        if not api_key:
            # For streaming, we can't easily raise an HTTPException if the stream has started.
            # We yield an error message instead.
            async def error_stream_no_keys():
                yield json.dumps({"error": {"message": "No available API keys in the proxy.", "code": 503}})
            return StreamingResponse(error_stream_no_keys(), media_type="application/json", status_code=503)

        request_data = await request.json()
        client = GeminiClient(api_key=api_key)
        
        async def stream_generator():
            async for chunk in client.stream_generate_content_native(model, request_data):
                yield chunk
        
        return StreamingResponse(stream_generator(), media_type="application/json")
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON in request body")
    except Exception as e:
        async def error_stream():
            yield json.dumps({"error": {"message": str(e), "code": 500}})
        return StreamingResponse(error_stream(), media_type="application/json", status_code=500)
