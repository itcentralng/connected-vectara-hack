import os
from langchain.vectorstores.vectara import Vectara

from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.tools import Tool
from langchain.agents import initialize_agent
from langchain.agents.types import AgentType
from langchain.schema import HumanMessage, AIMessage


def do_search(question, language, history=[]):
    docsearch = Vectara(os.getenv("VECTARA_CUSTOMER_ID"), os.getenv("VECTARA_CORPUS_ID"), os.getenv("VECTARA_API_KEY"))

    llm = ChatOpenAI()
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=docsearch.as_retriever(),
    )

    system_message = f"""
            "You are a helpful health expert."
            "You provide assistant to users on health matters"
            "You can ask questions to help you understand and diagnose a problem."
            "Try to sound as human as possible"
            "Make your responses as concise as possible"
            "Your response must be in {language} language"
            """
    tools = [
        Tool(
            name="Health Assistant",
            func=qa.run,
            description=f"Useful when you need to answer health related questions",
        )
    ]
    executor = initialize_agent(
        agent = AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        tools=tools,
        llm=llm,
        handle_parsing_errors="Check your output and make sure it conforms!",
        agent_kwargs={"system_message": system_message},
        verbose=True,
    )

    q = {"question": question}

    chat_history = []
    for h in history:
        chat_history.append(HumanMessage(content=h.question))
        chat_history.append(AIMessage(content=h.answer))

    return executor.run(input=q, chat_history=chat_history)