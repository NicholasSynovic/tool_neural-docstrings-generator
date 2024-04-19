from langchain_community.llms.ollama import Ollama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables.base import RunnableSequence
from pathlib import Path
from typing import List

def readFile(path: Path)    ->  str:
    with open(file=path, mode="r") as sourceFile:
        code: List[str] = sourceFile.readlines()
        sourceFile.close()

    return "".join(code)


def segmentFunctions(code: str) ->  List[str]:
    return [c.strip() for c in code.split(sep="def ")[1:]]


def main()    ->  None:
    systemPrompt: str = "This file contains code for counting lines of code of software projects. Generate suitable docstring for these Python functions. Do not explain the result"

    code: str = readFile(path=Path("./scc.py.test"))
    functions: List[str] = segmentFunctions(code=code)


    output_parser = StrOutputParser()
    chatPrompt: ChatPromptTemplate = ChatPromptTemplate.from_messages([
        ("system", systemPrompt),
        ("user", "{input}")
    ])

    llm: Ollama = Ollama(model="llama2")
    
    chain: RunnableSequence = chatPrompt | llm | output_parser

    print(chain.invoke({"input": functions[1]}))


if __name__ == "__main__":
    main()

