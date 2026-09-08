# AI Document Generator

An AI-powered document processing application that allows users to upload documents and generate useful information such as summaries, important details, and skills using Artificial Intelligence.

## Features

* Upload documents through a web interface
* Extract text from uploaded documents
* Generate AI-powered document summaries
* Extract important information from documents
* Identify relevant skills and keywords
* AI agent-based document processing
* MCP (Model Context Protocol) integration
* FastAPI backend
* Simple and user-friendly web interface

## Technologies Used

* **Python** – Backend programming
* **FastAPI** – Web framework and REST API
* **Google Gemini** – AI/LLM for document analysis
* **MCP (Model Context Protocol)** – AI agent and tool integration
* **HTML** – Frontend structure
* **CSS** – Frontend styling
* **JavaScript** – Frontend functionality
* **Uvicorn** – ASGI server
* **python-dotenv** – Environment variable management

## Project Structure

```text
AI-Document-Generator/
│
├── app.py
├── agent.py
├── mcp_server.py
├── document_processor.py
├── prompts.py
├── requirements.txt
├── .gitignore
├── README.md
│
├── templates/
│   └── index.html
│
├── static/
│   ├── style.css
│   └── script.js
│
└── uploads/
```

## File Description

### app.py

The main FastAPI application.

It is responsible for:

* Starting the web application
* Handling document uploads
* Calling document-processing functions
* Communicating with the AI agent
* Returning results to the frontend

### agent.py

Contains the AI agent logic.

The agent processes the extracted document text and uses the configured AI model to generate useful information from the document.

### mcp_server.py

Contains the MCP server implementation.

MCP is used to organize communication between the AI agent and the tools available in the application.

### document_processor.py

Responsible for processing uploaded documents and extracting their text.

The extracted text is then passed to the AI agent for further analysis.

### prompts.py

Contains the prompts used to instruct the AI model.

Keeping prompts in a separate file makes it easier to modify and improve the AI's responses.

### templates/index.html

Contains the main HTML page and user interface of the application.

### static/style.css

Contains the styling and layout of the web application.

### static/script.js

Contains the JavaScript code responsible for frontend interactions and communication with the FastAPI backend.

### requirements.txt

Contains the Python packages required to run the application.

## Application Workflow

```text
User
  │
  ▼
Upload Document
  │
  ▼
FastAPI Backend
  │
  ▼
Document Processor
  │
  ▼
Extract Document Text
  │
  ▼
AI Agent
  │
  ▼
Google Gemini / MCP
  │
  ▼
Generate Document Insights
  │
  ▼
Return Result
  │
  ▼
Display Result to User
```

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Nagashree13/AI-Document-Generator.git
```

Navigate to the project directory:

```bash
cd AI-Document-Generator
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
```

Activate the virtual environment on Linux/macOS:

```bash
source venv/bin/activate
```

For Windows:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## API Key Configuration

The application requires an API key for the AI model.

Create a `.env` file in the project directory:

```text
.env
```

Add your API key:

```env
GEMINI_API_KEY=your_api_key_here
```

The application reads the API key from the environment variables.



## Running the Application

Start the FastAPI server using:

```bash
uvicorn app:app --reload
```

After starting the server, open the application in your browser:

```text
http://127.0.0.1:8000
```

## How to Use

1. Open the AI Document Generator in your browser.
2. Upload a document.
3. The application extracts the text from the document.
4. The extracted text is processed by the AI agent.
5. Google Gemini analyzes the document.
6. The generated information is returned to the application.
7. The result is displayed on the web interface.

## Example

For a resume uploaded to the application, the AI can generate information such as:

```text
Summary:
MCA graduate with experience in Python, AI and web development.

Skills:
- Python
- SQL
- FastAPI
- MySQL
- JavaScript
- AI/ML
```




## Future Improvements

* Support for additional document formats
* Chat with uploaded documents
* Document question answering
* Document comparison
* Advanced keyword extraction
* User authentication and authorization
* Database integration
* Cloud deployment
* Additional MCP tools
* Improved AI response generation

## Project Objective

The objective of this project is to demonstrate the integration of **Generative AI, AI agents, MCP, document processing, and web development** to build a practical AI-based document analysis application.

This project demonstrates experience in:

* Python development
* FastAPI
* Generative AI
* Google Gemini
* MCP
* Document processing
* Prompt engineering
* REST APIs
* Frontend-backend integration

## Author

**Nagashree M.K.**

MCA Graduate

## License

This project is created for educational and demonstration purposes.
