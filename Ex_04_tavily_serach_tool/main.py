from dotenv import load_dotenv
load_dotenv()

from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch

llm = ChatOpenAI()
tools=[TavilySearch()]
agent = create_agent(model=llm,tools=tools)
def main():
    print("Hello from langchain-course!")
    result=agent.invoke({"messages":HumanMessage(content="search for 3 job postings with terraform, devops with >6YOE in the hyderabd on linkedin and posted in less than 1 week and list their details")})
    print(result)


if __name__ == "__main__":
    main()
