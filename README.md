# 📚 BOOKS_AGENT

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Web%20App-FF4B4B?logo=streamlit)
![OpenRouter](https://img.shields.io/badge/OpenRouter-LLM-success)
![Google Books API](https://img.shields.io/badge/API-Google%20Books-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

An AI-powered Book Search Assistant built with **Python**, **OpenRouter LLM**, **Google Books API**, and **Streamlit**. The application enables users to search for books using natural language, retrieves real-time book information from the Google Books API, and presents the results through an intuitive web interface or command-line application.

---

# Overview

BOOKS_AGENT combines the reasoning capabilities of a Large Language Model with the Google Books API through **Function Calling (Tool Calling)**.

The assistant understands user requests such as book titles, authors, genres, topics, or recommendations, automatically invokes the appropriate search tool, and formats the results into a clean and readable response.

The project is available in both:

* **Command-Line Interface (CLI)**
* **Interactive Streamlit Web Application**

---

# Features

* AI-powered conversational book search
* Search books by title, author, topic, keyword, or genre
* Google Books API integration
* OpenRouter LLM with Function Calling
* Persistent conversation memory
* Interactive Streamlit web application
* Command-line interface
* Search history support
* Dark and Light UI themes
* Clean, formatted book results

---

# Technology Stack

| Category      | Technology       |
| ------------- | ---------------- |
| Language      | Python           |
| LLM           | OpenRouter       |
| API           | Google Books API |
| Web Framework | Streamlit        |
| HTTP Client   | Requests         |
| Environment   | python-dotenv    |
| Storage       | JSON             |

---

# System Architecture

```text
                    User
                      │
                      ▼
             Streamlit UI / CLI
                      │
                      ▼
             Book Search Agent
                      │
         ┌────────────┴────────────┐
         ▼                         ▼
   OpenRouter LLM          Google Books API
         │                         │
         └────────────┬────────────┘
                      ▼
             Formatted Response
                      │
                      ▼
                    User
```

---

# Project Structure

```text
BOOKS_AGENT/
│
├── main.py                  # CLI application
├── streamlit_app.py         # Streamlit UI
├── tools.py                # Google Books API tool
├── prompt.py               # System prompt
├── memory.py               # Memory management
├── memory.json             # Conversation history
├── .env                    # API keys
├── requirements.txt
├── images/
│   ├── home-page.png
│   ├── search-results.png
│   ├── cli-search.png
│   └── non-book-query.png
└── README.md
```

---

# Installation

Clone the repository

```bash
git clone https://github.com/adithyaavenkatesh15/BOOKS_AGENT.git
```

Navigate into the project directory

```bash
cd BOOKS_AGENT
```

Create a virtual environment

```bash
python -m venv venv
```

Activate the environment

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Setup

Create a `.env` file inside the project root.

```env
OPENROUTER_API_KEY=your_openrouter_api_key
GOOGLE_BOOKS_API_KEY=your_google_books_api_key
```

### Obtain API Keys

**OpenRouter**

https://openrouter.ai/

**Google Books API**

https://developers.google.com/books

---

# Running the Application

## Command-Line Interface

```bash
python main.py
```

Example Queries

```
Search Atomic Habits

Find Harry Potter

Books by James Clear

Best Python books

Top Machine Learning books

Find Ikigai books
```

---

## Streamlit Web Application

```bash
streamlit run streamlit_app.py
```

The application will open in your browser at:

```
http://localhost:8501
```

---

# How It Works

1. The user enters a natural language query.
2. The OpenRouter LLM interprets the request.
3. The model invokes the Book Search Tool.
4. The tool queries the Google Books API.
5. The retrieved book information is returned to the LLM.
6. The LLM formats the results into a readable response.
7. Conversation history is stored locally for future interactions.

---

# Screenshots

## Home Page

The modern Streamlit interface provides a clean and intuitive experience for searching books.

```text
images/home-page.png
```

![Home Page](images/home-page.png)

---

## Search Results

Example of searching for **Ikigai** books using natural language.

```text
images/search-results.png
```

![Search Results](images/search-results.png)

---

## Command-Line Interface

Terminal-based interaction with the Book Search Agent.

```text
images/cli-search.png
```

![CLI Version](images/cli-search.png)

---

## Handling Non-Book Queries

The assistant gracefully responds to questions outside its supported domain.

```text
images/non-book-query.png
```

![Non Book Query](images/non-book-query.png)

---

# Memory

Conversation history is stored locally in **memory.json**.

You can delete or clear this file at any time to reset the assistant's memory.

---

# Future Enhancements

* Personalized recommendations
* Reading list management
* Favorite books
* Book summaries
* Voice-based interaction
* Multi-language support
* Goodreads integration
* RAG-powered semantic search
* User authentication

---

# License

This project is licensed under the **MIT License**.

---

# Author

**Adithya A. Venkatesh**

GitHub: https://github.com/adithyaavenkatesh15

LinkedIn: *(Add your LinkedIn profile here.)*

---

# Acknowledgements

* OpenRouter
* Google Books API
* Streamlit
* Python Community

---

# Support

If you find this project useful, consider giving it a ⭐ on GitHub. Your support helps others discover the project and encourages future development.

