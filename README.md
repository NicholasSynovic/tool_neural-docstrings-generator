# Neural Docstring Generator (`ndg`)

> A small program to generate docstrings using Ollama-compatible LLMs

## Table of Contents

- [Neural Docstring Generator (`ndg`)](#neural-docstring-generator-ndg)
  - [Table of Contents](#table-of-contents)
  - [About](#about)
  - [How to Install](#how-to-install)
    - [Dependencies](#dependencies)
  - [How to Run](#how-to-run)
  - [Default LLM](#default-llm)
  - [Default System Prompt](#default-system-prompt)

## About

I don't like writing docstrings.

Large language models (LLMs) don't complain about writing docstrings.

Therefore, if I can get LLMs to write docstrings for me, then I'll be happy and
free!

This tool (neural docstring generator, or `ndg`) is meant to provide a proof of
concept on how to:

- Read in source code files
- Extract functions and their supporting code from the source file
- Inference with LLMs self-hosted via Ollama with LangChain

## How to Install

`ndg` was tested to work on x86-64 Linux computers running `Python3.10`.

To install:

1. `git clone` this repository
1. `cd` into this repository
1. Install dependencies with `pip install -r requirements && poetry install`
1. Build and install the `ndg` tool with `make`

### Dependencies

The following dependencies are required:

- `python3.10`
- `poetry`
- `langchain`
- `progress`
- `click`
- [`pyfs`](https://github.com/NicholasSynovic/python-fs-utils%22)

## How to Run

```shell
Usage: ndg [OPTIONS]

Options:
  -i, --input PATH   Source file to generate docstrings for  [required]
  -m, --model TEXT   LLM used to generate docstrings. NOTE: Must be
                     recognizable by Ollama
  -s, --system TEXT  The system prompt to use
  -o, --output PATH  File to output docstrings to  [required]
  --help             Show this message and exit.
```

If your `input` and `output` are equivalent, then a new file will be created in
the same directory as `input`, but with the `.ndg` file extension appended to
avoid overwriting content between the two files.

## Default LLM

By default,
[Ollama's default CodeGemma model (`codegemma`)](https://ollama.com/library/codegemma)
is used for this tool.

## Default System Prompt

Here is the default system prompt.

```text
This file contains code for counting lines of code of software projects.
Generate suitable docstring for these Python functions in Google's style.
Do not explain the result.
Only return the docstring and function declaration.
Return as raw text.
```

This can be adjusted with `ndg --system`
