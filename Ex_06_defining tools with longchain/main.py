#from typing import List
#from pydantic import BaseModel,Field

from dotenv import load_dotenv
load_dotenv()

from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from langchain_tavily import TavilySearch
from schemas import AgentResponse

tools=[TavilySearch()]
model=ChatOpenAI(model="gpt-4")

#create react-gent                                                        
agent = create_agent(model,tools=tools, response_format=AgentResponse)


def main():
    print("Hello from langchain-course!")
    result=agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": "search for 3 job postings with terraform, devops with >6YOE in the hyderabd on linkedin and posted in less than 1 week and list their details"
                }           
            ]
        }
    )
    print(result["structured_response"])


if __name__ == "__main__":
    main()
