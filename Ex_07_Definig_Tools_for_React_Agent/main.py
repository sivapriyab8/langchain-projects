from dotenv import load_dotenv
from langchain.tools import tool
from typing import List

from langchain_core.messages import HumanMessage, ToolMessage
from langchain_core.tools import Tool, tool
from langchain_openai import ChatOpenAI
from callbacks import AgentCallbackHandler


load_dotenv()

@tool
def get_text_length(text:str)-> int:
    """Returns the length of a text by characters"""
    print(f"get_ext_length enter with {text=}")
    text = text.strip("'\n").strip('"') #stripping away non-alphabetic characters just in case
    return len(text)

def find_tool_by_name(tools: List[Tool], tool_name: str)-> Tool:
    for tool in tools:
        if tool.name == tool_name:
            return tool
    raise ValueError(f"Tool with name {tool_name} not found")

if __name__ == '__main__':
    #print("Hello ReAct LangChain!")
    print("Hello LangChain Tools (.bind_tools)!")
    #print(get_text_length(text="Dog"))
    tools = [get_text_length]

    ''' 
    template = """
    Answer the following questions as best you can. You have access to the following tools:

    {tools}

    Use the following format:

    Question: the input question you must answer
    Thought: you should always think about what to do
    Action: the action to take, should be one of [{tool_names}]
    Action Input: the input to the action
    Observation: the result of the action
    ... (this Thought/Action/Action Input/Observation can repeat N times)
    Thought: I now know the final answer
    Final Answer: the final answer to the original input question

    Begin!

    Question: {input}
    Thought:
    """

    prompt = PromptTemplate.from_template(template=template).partial(
        tools=render_text_description(tools), tool_names=",".join([t.name for t in tools])
    )
    '''

    llm = ChatOpenAI(
        temperature=0,
        callbacks=[AgentCallbackHandler()],
    )
    llm_with_tools = llm.bind_tools(tools)

    #start Conversation
    messages = [HumanMessage(content="Waht is the length of the word: DOG")]

    while True:
        ai_message = llm_with_tools.invoke(messages)

        #if the model decides to 
        tool_calls = getattr(ai_message,"tool_calls",None) or []
        if len(tool_calls)>0:
            messages.append(ai_message)
            for tool_call in tool_calls:
                #tool_call is typically a dict with keys: id, type, name, args
                tool_name = tool_call.get("name")
                tool_args = tool_call.get("args", {})
                tool_call_id = tool_call.get("id")
                tool_to_use = find_tool_by_name(tools,tool_name)
                observation = tool_to_use.invoke(tool_args)
                print(f"observation={observation}")

                messages.append(
                    ToolMessage(content=str(observation), tool_call_id=tool_call_id)
                )
            continue
        #no tool calls->final answer
        print(ai_message.content)
        break