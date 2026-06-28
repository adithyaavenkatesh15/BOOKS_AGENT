# BOOKS_AGENT

BOOKS_AGENT is an AI-powered book search assistant that helps users discover books using natural language queries. It combines an LLM-powered agent with the Google Books API to provide relevant book results and present them in a clean, user-friendly format.

## Overview

This project contains two main ways to interact with the agent:

- A terminal-based chatbot experience through [main.py](main.py)
- A modern web interface through [streamlit_app.py](streamlit_app.py)

The assistant is designed to understand requests such as book titles, authors, topics, genres, or general book recommendations and then fetch matching results from the Google Books API.

## Features

- Search books by title, author, topic, keyword, or genre
- Use an AI assistant to interpret user requests
- Format results clearly with title, author, publisher, and publication date
- Store recent searches and conversation memory locally
- Provide a polished Streamlit-based user interface

## Project Structure

- [main.py](main.py) - Contains the core agent loop, tool calling logic, and API integration
- [tools.py](tools.py) - Implements the Google Books search tool
- [prompt.py](prompt.py) - Defines the system prompt for the assistant
- [memory.py](memory.py) - Handles loading and saving local memory
- [streamlit_app.py](streamlit_app.py) - Provides the web app UI
- [memory.json](memory.json) - Stores the agent memory locally

## Prerequisites

Make sure you have Python installed on your machine.

Then install the required packages:

```bash
pip install requests python-dotenv streamlit
```

## Environment Setup

Create a `.env` file inside the BOOKS_AGENT folder and add your API keys:

```env
OPENROUTER_API_KEY=your_openrouter_api_key
GOOGLE_BOOKS_API_KEY=your_google_books_api_key
```

### Where to get the keys

- OpenRouter API key: https://openrouter.ai/
- Google Books API key: https://developers.google.com/books

## Running the Agent

### 1. Run the terminal version

From the BOOKS_AGENT folder, run:

```bash
python main.py
```

You can then type prompts such as:

- Search Atomic Habits
- Find Harry Potter
- Books by James Clear
- Best Python books
- Top machine learning books

### 2. Run the Streamlit web app

From the BOOKS_AGENT folder, run:

```bash
streamlit run streamlit_app.py
```

This will launch the web interface in your browser.

## How It Works

1. The user enters a query.
2. The LLM interprets the request.
3. The agent calls the book search tool.
4. The Google Books API returns book results.
5. The AI formats the output in a friendly response.

## Memory

The app stores conversation memory locally in [memory.json](memory.json). You can clear or delete this file if you want to reset the assistant memory.

## Notes

- The assistant is focused on book-related queries.
- For unrelated questions, it will politely respond that it can only help with books.
- Make sure your API keys are valid and available in the `.env` file before running the app.
