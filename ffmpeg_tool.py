

import asyncio
import subprocess
from typing import Optional 
from langchain.callbacks.manager import (
    CallbackManagerForToolRun,
    AsyncCallbackManagerForToolRun,
)
from langchain.tools import BaseTool 

class FfmpegTool(BaseTool):
    name = "FfmpegTool"
    description = "useful for when you need to edit and manipulate audio files with ffmpeg"

    def _run(
        self, 
        query: str, 
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        query_items = query.split(" ")
        if query_items[0] == "ffmpeg":
            query_items = query_items[1:]

        full_cmd = ["ffmpeg"] + query_items
        subprocess.run(full_cmd),

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
            async def async_run(cmd):
                proc = await asyncio.create_subprocess_shell(
                    cmd,
                    stdout=asyncio.subprocess.PIPE,
                    stderr=asyncio.subprocess.PIPE,
                )

                stdout, stderr = await proc.communicate()

                print(f'[{cmd!r} exited with {proc.returncode}]')
                if stdout:
                    print(f'[stdout]\n{stdout.decode()}')
                if stderr:
                    print(f'[stderr]\n{stderr.decode()}')

            query_items = query.split(" ")
            if query_items[0] == "ffmpeg":
                query_items = query_items[1:]

            full_cmd = ["ffmpeg"] + query_items
            await async_run(full_cmd),

            return {
                "output": "This is a test",
                "intermediate_steps": [
                    "This is a test",
                    "This is a test",
                    "This is a test",
                    "This is a test",
                ],
            }
