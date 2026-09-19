# Hospital Support Agent

An AI-powered hospital support agent built with LangChain, Streamlit, and SQLite. This intelligent agent helps patients find the right hospital services through natural language queries.

## Features

- **AI-Powered Conversational Interface**: Natural language processing for patient queries
- **4 Integrated Tools**: Search functionalities, category listing, and step-by-step guidance
- **SQLite Database**: 24 hospital services across 7 categories
- **LM Studio Integration**: Local LLM support for privacy and control
- **Streamlit UI**: Modern, user-friendly chat interface
- **Smart Query Routing**: Automatically categorizes and routes patient requests

## Hospital Services Categories

The agent supports services across 7 categories:
- 📅 **Appointments**: Schedule, cancel, reschedule, walk-in visits
- 📋 **Medical Records**: Test results, prescriptions, medical history
- 💳 **Billing & Insurance**: Payments, claims, coverage verification
- 🚨 **Emergency**: ER guidance, ambulance services
- 💊 **Pharmacy**: Prescription refills, drug information, OTC medications
- 🏥 **Inpatient**: Admission, discharge, room service
- 🔗 **Referrals**: Specialist referrals, second opinions

## Technology Stack

- **Backend**: Python, LangChain
- **Frontend**: Streamlit
- **Database**: SQLite
- **LLM**: LM Studio (local)
- **AI Framework**: LangChain OpenAI

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Mahsa-Arjmand/Agent-operator-.git
cd Agent-operator-
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables (optional):
Create a `.env` file in the project root:
```
LM_STUDIO_API_BASE=http://localhost:1234/v1
LM_STUDIO_API_KEY=lm-studio
LM_STUDIO_MODEL=gemma
```

## Usage

1. Start LM Studio server (default: `http://localhost:1234/v1`)

2. Run the Streamlit application:
```bash
streamlit run app.py
```

3. Open your browser and interact with the hospital support agent

## Example Queries

Try these natural language queries:
- "I need to see a doctor"
- "Show all services"
- "My test results"
- "How much do I owe"
- "Need ambulance"
- "Refill my prescription"
- "I'm being discharged"
- "Need specialist referral"

## Project Structure

```
Agent-operator-/
├── agent.py          # Main agent logic and routing
├── app.py            # Streamlit frontend application
├── config.py         # Configuration and environment variables
├── database.py       # SQLite database operations
├── tools.py          # LangChain tools for agent
├── requirements.txt  # Python dependencies
├── data/             # Database files
└── README.md         # This file
```

## How It Works

1. **Query Processing**: The agent analyzes user queries using natural language processing
2. **Tool Selection**: Automatically selects the appropriate tool based on query intent:
   - `search_functionalities`: Semantic search for hospital services
   - `get_steps`: Retrieves step-by-step procedures
   - `list_categories`: Shows all available service categories
   - `search_by_keyword`: Quick keyword-based search
3. **Response Generation**: Uses LM Studio to generate friendly, contextual responses
4. **Database Integration**: SQLite database stores 24 hospital services with detailed procedures

## Customization

- **Add New Services**: Modify the database seeding in `database.py`
- **Change LLM Model**: Update `LM_STUDIO_MODEL` in `.env` file
- **Modify Tools**: Extend functionality in `tools.py`
- **Custom UI**: Edit the Streamlit interface in `app.py`

## Requirements

- Python 3.8+
- LM Studio (for local LLM)
- Dependencies listed in `requirements.txt`

## License

This project is open source and available for educational and commercial use.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Contact

For questions or suggestions, please open an issue on GitHub.
