
from typing import Optional, Type

from langchain.callbacks.manager import (
    CallbackManagerForToolRun,
    AsyncCallbackManagerForToolRun,
)
from langchain.tools import BaseTool 

class MirTool(BaseTool):
    name = "mir_tool"
    description = "useful for when you need to analyze audio or music"

    def _run(
        self, 
        query: str, 
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        return {
            "output": "This is a test",
            "intermediate_steps": [
                "This is a test",
                "This is a test",
                "This is a test",
                "This is a test",
            ],
        }

    async def _arun(
            self, 
            query: str, 
            run_manager: Optional[AsyncCallbackManagerForToolRun] = None
        ) -> str:
            """Use the tool asynchronously."""
            raise NotImplementedError("mir_tool does not support async")
