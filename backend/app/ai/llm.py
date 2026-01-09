from langchain_nvidia_ai_endpoints import ChatNVIDIA
from langchain.messages import HumanMessage
from fastapi.concurrency import run_in_threadpool
from app.core import settings
from app.ai.prompts import LAB_PROMPT

class NvidiaLLM:
    def __init__(self,
                 model_name: str="nvidia/nvidia-nemotron-nano-9b-v2", 
                 temp: float=.5, 
                 max_tokens:int= 4096):
        self.model = ChatNVIDIA(
            model_name=model_name,
            temp=temp,
            api_key=settings.NIM_API,
            max_tokens=max_tokens,
        )

    async def parse_labs(self, text: str) -> str:
        prompt = LAB_PROMPT + text
        response = await run_in_threadpool(
            self.model.invoke,
            [HumanMessage(prompt)],
        )
        return str(response.content)
