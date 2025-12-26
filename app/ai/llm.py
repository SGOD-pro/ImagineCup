
from langchain_nvidia_ai_endpoints import ChatNVIDIA
from app.config import settings
class NVDIALLM(ChatNVIDIA):
    def __init__(
        self,
        model_name: str,
        temp: float = 0.5,
        stream: bool = False,
        callback=None,
        **kwargs,
    ):
        super().__init__(
            model=model_name,
            api_key=settings.NIM_API,  # let environment or explicit override handle it
            temperature=temp,
            top_p=1.0,
            stream=stream,
            max_tokens=4096,
            
            **kwargs,
            
        )
