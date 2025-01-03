
from dotenv import load_dotenv
# from langchain.agents import AgentType, initialize_agent
# from langchain import hub
# from langchain.tools.render import render_text_description
# from tools.ffmpeg_tool import FfmpegTool

# from langchain_community.agent_toolkits.load_tools import load_tools
# from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

from tools.ffmpeg_tool import FfmpegTool
load_dotenv()


def main():
    # Create the agent
    memory = MemorySaver()
    model = ChatAnthropic(
        model_name="claude-3-sonnet-20240229",
        timeout=60,
        stop=None
    )
    # model = ChatOpenAI(name="gpt-4o-mini")
    search = TavilySearchResults(max_results=2)
    tools = [search, FfmpegTool()]

    prompt = """You are an expert audio engineer specializing in FFmpeg operations.
    When asked to perform audio operations:
    1. Use the FfmpegTool for any audio file manipulations
    2. Be precise with file paths, always using ./samples/ directory
    3. Verify the command's success and report any errors
    4. Only use valid FFmpeg parameters and syntax

    Remember to check the output of commands and handle any errors appropriately."""

    agent_executor = create_react_agent(model, tools, checkpointer=memory, state_modifier=prompt)

    # Use the agent
    config = {"configurable": {"thread_id": "abc123"}}
    for chunk in agent_executor.stream(
        {"messages": [HumanMessage(content="hi im bob! and i live in sf")]}, config
    ):
        print(chunk)
        print("----")

    for chunk in agent_executor.stream(
        {"messages": [HumanMessage(content="can you clip the audio file located at ./samples/helicopter.wav to be 5 seconds, save it as an mp3 file?")]},
        config,
    ):
        print(chunk)
        print("----")


if __name__ == '__main__':
    main()
