import re
from pathlib import Path
from typing import List

import click
from langchain_community.llms.ollama import Ollama
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.base import RunnableSequence
from progress.bar import Bar
from pyfs import resolvePath

SYSTEM_PROMPT: str = """This file contains code for counting lines of code of software projects.
Generate suitable docstring for these Python functions in Google's style.
Do not explain the result.
Only return the docstring and function declaration.
Return as raw text."""


def readFile(path: Path) -> str:
    """
    Reads a file and returns its contents as a string.

    Args:
        path: The path to the file.

    Returns:
        The contents of the file as a string.
    """
    with open(file=path, mode="r") as sourceFile:
        code: List[str] = sourceFile.readlines()
        sourceFile.close()

    return "".join(code)


def segmentFunctions(code: str) -> List[str]:
    """
    Splits the code into individual functions.

    Args:
        code: The code to be segmented.

    Returns:
        A list of function definitions.
    """
    return [c.strip() for c in code.split(sep="def ")[1:]]


def inference(
    systemPrompt: str,
    code: str,
    model: str = "codegemma",
) -> str:
    """
    Generates docstrings for given code using the specified model.

    Args:
        systemPrompt: The system prompt to use.
        code: The code to generate docstrings for.
        model: The LLM model to use. Defaults to "codegemma".

    Returns:
        The generated docstrings.
    """
    output_parser = StrOutputParser()
    chatPrompt: ChatPromptTemplate = ChatPromptTemplate.from_messages(
        [("system", systemPrompt), ("user", "{input}")]
    )

    llm: Ollama = Ollama(model=model)

    chain: RunnableSequence = chatPrompt | llm | output_parser

    return chain.invoke({"input": code})


@click.command()
@click.option(
    "-i",
    "--input",
    "sourceFile",
    type=Path,
    required=True,
    help="Source file to generate docstrings for",
)
@click.option(
    "-m",
    "--model",
    "model",
    type=str,
    required=False,
    default="codegemma",
    help="LLM used to generate docstrings. NOTE: Must be recognizable by Ollama",
)
@click.option(
    "-s",
    "--system",
    "systemPrompt",
    type=str,
    required=False,
    default=SYSTEM_PROMPT,
    help="The system prompt to use",
)
@click.option(
    "-o",
    "--output",
    "output",
    type=Path,
    required=True,
    help="File to output docstrings to",
)
def main(
    systemPrompt: str,
    sourceFile: Path,
    output: Path,
    model: str,
) -> None:
    """
    Generates docstrings for functions in a given source file.

    Args:
        systemPrompt: The prompt to use for the docstring generation model.
        sourceFile: The path to the source file.
        output: The path to the output file.
        model: The name of the docstring generation model to use.

    Returns:
        None
    """
    data: List[str] = []
    sf: Path = resolvePath(path=sourceFile)
    output: Path = resolvePath(path=output)

    if output == sf:
        output = output.with_suffix(suffix=".ndg")

    code: str = readFile(path=sf)
    functions: List[str] = segmentFunctions(code=code)

    with Bar("Generating docstrings...", max=len(functions)) as bar:
        func: str
        for func in functions:
            data.append(inference(systemPrompt=systemPrompt, code=func, model=model))
            bar.next()

    with open(file=output, mode="w") as outputFile:
        code: str
        for code in data:
            formattedCode: str = (
                re.sub(
                    r"^.*`.*\n?",
                    "",
                    code,
                    flags=re.MULTILINE,
                )
                + "\n\n"
            )
            outputFile.write(formattedCode)
        outputFile.close()


if __name__ == "__main__":
    main()
