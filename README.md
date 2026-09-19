# Hospital Support Agent

An AI-powered hospital support agent that helps patients find the right hospital services. This agentic workflow automation system uses LangChain with local LLM models (LM Studio) and provides intelligent responses to patient queries.

## Features

- **AI-Powered Conversations**: Uses LangChain with local LLM (LM Studio) for natural language understanding
- **7 Service Categories**: Covers appointments, medical records, billing, emergency, pharmacy, inpatient, and referrals
- **22 Hospital Services**: Comprehensive database of hospital workflows and procedures
- **Intelligent Search**: Keyword-based and functionality-based search with fuzzy matching
- **Friendly Interface**: Built with Streamlit for an intuitive chat interface
- **Tool Integration**: 4 specialized tools for database operations and information retrieval

## Architecture

```
User Query → Hospital Agent → Tools → SQLite Database
```

### Components

- **Agent System** (`agent.py`): Main AI agent with intelligent query routing
- **Database** (`database.py`): SQLite database with hospital services and workflows
- **Tools** (`tools.py`): 4 specialized tools for database operations
- **Web Interface** (`app.py`): Streamlit-based chat interface
- **Configuration** (`config.py`): LM Studio API configuration

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Mahsa-Arjmand/Agentic-Workflow-Automation.git
cd Agentic-Workflow-Automation
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure LM Studio:
- Install and run LM Studio
- Start the LM Studio server
- Update `config.py` with your LM Studio API settings:
```python
LM_STUDIO_API_BASE = "http://localhost:1234/v1"
LM_STUDIO_API_KEY = "your-api-key"
LM_STUDIO_MODEL = "your-model-name"
```

## Usage

Run the Streamlit application:
```bash
streamlit run app.py
```

The application will start at `http://localhost:8501`

## Example Queries

- "I need to see a doctor"
- "show all services"
- "my test results"
- "how much do I owe"
- "need ambulance"
- "refill my prescription"
- "I'm being discharged"
- "need specialist referral"

## Service Categories

| Category | Services |
|----------|----------|
| 📅 Appointments | Schedule, cancel, reschedule, walk-in |
| 📋 Medical Records | Test results, prescriptions, history |
| 💰 Billing & Insurance | Payment, claims, coverage |
| 🚨 Emergency | ER guide, ambulance |
| 💊 Pharmacy | Refills, drug info, OTC |
| 🏥 Inpatient | Admission, discharge, room service |
| 👨‍⚕️ Referrals | Specialist, second opinion |

## Tools

The agent uses 4 specialized tools:

1. **`search_functionalities`**: Searches hospital services by functionality
2. **`get_steps`**: Retrieves detailed steps for a specific service
3. **`list_categories`**: Lists all available service categories
4. **`search_by_keyword`**: Quick keyword-based search

## Technology Stack

- **Framework**: Streamlit
- **AI/ML**: LangChain, LangChain OpenAI
- **Database**: SQLite
- **LLM**: LM Studio (local LLM)
- **Language**: Python

## Configuration

Edit `config.py` to customize:

```python
LM_STUDIO_API_BASE = "http://localhost:1234/v1"
LM_STUDIO_API_KEY = "your-api-key"
LM_STUDIO_MODEL = "your-model-name"
```

## Database

The SQLite database is automatically initialized with sample data on first run. It includes:
- 7 service categories
- 22 hospital services with detailed workflows
- Step-by-step procedures for each service

## Project Structure

```
.
├── agent.py          # Main AI agent
├── app.py            # Streamlit web interface
├── config.py         # Configuration settings
├── database.py       # Database operations
├── tools.py          # Agent tools
├── requirements.txt  # Python dependencies
├── data/            # Database files (auto-generated)
└── README.md        # This file
```

## License

This project is open source and available under the MIT License.

## Author

Mahsa Arjmand
