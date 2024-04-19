from langchain_community.llms.ollama import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.base import RunnableSequence

def main(systemPrompt: str, prompt: str)    ->  None:
    output_parser = StrOutputParser()
    chatPrompt: ChatPromptTemplate = ChatPromptTemplate.from_messages([
        ("system", systemPrompt),
        ("user", "{input}")
    ])

    llm: Ollama = Ollama(model="llama2")
    
    chain: RunnableSequence = chatPrompt | llm | output_parser

    print(chain.invoke({"input": prompt}))


if __name__ == "__main__":
    main()

