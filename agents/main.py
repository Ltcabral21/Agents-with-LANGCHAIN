from langchain.chat_models import ChatOpenAI
from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder
)
from langchain.schema import SystemMessage
from langchain.agents import OpenAIFunctionsAgent, AgentExecutor
from dotenv import load_dotenv

from tools.sql import list_tables, run_query_tool, describe_tables_tool

load_dotenv()

chat = ChatOpenAI()

tables = list_tables()
print(tables)
prompt = ChatPromptTemplate(
    messages=[
        SystemMessage(content = f"You are an AI which has access to a SQLite database.\n(tables)"),
        HumanMessagePromptTemplate.from_template("{input}"),
        MessagesPlaceholder(variable_name="agent_scratchpad")
    ]
)

tools = [run_query_tool, describe_tables_tool]

agent = OpenAIFunctionsAgent(
    llm=chat,
    prompt=prompt,
    tools=tools
)

agent_executor = AgentExecutor(
    agent=agent,
    verbose=True,
    tools=tools
)

agent_executor("how many threes does the world have?")