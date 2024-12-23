

import asyncio
import subprocess
from typing import Optional
from langchain.callbacks.manager import (
    CallbackManagerForToolRun,
    AsyncCallbackManagerForToolRun,
)
from langchain.tools import BaseTool
from langchain.chains import LLMChain
from langchain.llms import OpenAI
from langchain.prompts import PromptTemplate


class FfmpegTool(BaseTool):
    name: str = "FfmpegTool"
    description: str = """Tool for audio file manipulation using FFmpeg.
    Can perform operations like:
    - Clipping audio files to specific durations
    - Converting between audio formats
    - Adjusting audio quality and bitrate
    - Extracting audio from video
    Input should be a clear description of the desired audio operation."""

    def _run(
        self,
        query: str,
        run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Use the tool."""
        template = """Question or Query: {query}

  Generate a valid ffmpeg command to accomplish this task.
    Only return the command itself, no explanations or additional text.
    Use relative paths starting with ./samples/ for input and output files.
        """

        prompt = PromptTemplate(template=template, input_variables=["query"])
        llm = OpenAI()
        llm_chain = LLMChain(prompt=prompt, llm=llm)
        command: str = llm_chain.run(query).strip()

        # Split the command and remove any extra whitespace or newlines
        cmd_parts = [part.strip() for part in command.split() if part.strip()]

        if not cmd_parts or cmd_parts[0] != "ffmpeg":
            return "Invalid command generated"


        # Remove 'ffmpeg' if it's the first part and add our standard flags
        if cmd_parts[0] == "ffmpeg":
            cmd_parts = cmd_parts[1:]

        full_cmd = ["ffmpeg", "-loglevel", "error", "-y"] + cmd_parts

        print(f'\n\nrunning command: {" ".join(full_cmd)}')
        output = subprocess.run(full_cmd, capture_output=True),

        if type(output) == tuple:
            output = output[0]

        stdout = output.stdout
        stderr = output.stderr
        returncode = output.returncode
        print(f'[ffmpeg exited with {returncode}]')
        if stdout:
            print(f'\n{stdout.decode()}')
        if stderr:
            return f'[there was an error]\n{stderr.decode()}'

        return stdout.decode()

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
                    raise Exception(f'[stderr]\n{stderr.decode()}')

                return stdout

            query_items = query.split(" ")
            if query_items[0] == "ffmpeg":
                query_items = query_items[1:]

            full_cmd = ["ffmpeg"] + query_items
            await async_run(full_cmd),

            return "output of this was saved to ./output.wav"
