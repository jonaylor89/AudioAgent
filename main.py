
from langchain.agents import AgentType, initialize_agent, load_tools
from langchain.llms import OpenAI
from langchain import hub
# from langchain.agents.format_scratchpad import format_log_to_str
# from langchain.agents.output_parsers import ReActSingleInputOutputParser
from langchain.tools.render import render_text_description
# from langchain.tools import Tool
# from langchain.agents import AgentExecutor
from dotenv import load_dotenv
# from tools.mir_tool import MusicInformationRetrievalTool
from tools.ffmpeg_tool import FfmpegTool
# from tools.reverb_tool import ReverbTool
# import os

# os.environ["LANGCHAIN_TRACING"] = "true"

def main():
    llm = OpenAI(temperature=0)
    tools = load_tools(["serpapi", "llm-math"], llm=llm)
    # tools.append(MusicInformationRetrievalTool())
    tools.append(FfmpegTool())
    # tools.append(ReverbTool)

    prompt = hub.pull("hwchase17/react")
    prompt = prompt.partial(
        tools=render_text_description(tools),
        tool_names=", ".join([t.name for t in tools]),
    )
    # llm_with_stop = llm.bind(stop=["\nObservation"])
    # agent = (
    #     {
    #         "input": lambda x: x["input"],
    #         "agent_scratchpad": lambda x: format_log_to_str(x["intermediate_steps"]),
    #     }
    #     | prompt
    #     | llm_with_stop
    #     | ReActSingleInputOutputParser()
    # )

    # agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    agent_executor = initialize_agent(
        tools, 
        llm, 
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
        verbose=True,
        handle_parsing_errors=True, 
    )
    agent_executor.invoke(
        {
            "input": "can you clip the audio file located at input.wav to be 5 seconds, save it as an mp3 file?",
        }
    )


if __name__ == '__main__':
    load_dotenv()
    main()