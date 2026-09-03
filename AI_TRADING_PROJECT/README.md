# AI Trading Agent

An AI-powered trading workflow built with **FastAPI, LangGraph, PostgreSQL, and LLM-based market analysis**.

The project demonstrates how an agentic workflow can analyze simulated market data, generate a trade proposal, pause for **human approval**, and execute the approved trade through a broker service.

> **Note:** This is an educational/simulated trading project. It does not connect to a real brokerage account or execute real financial transactions.

---

## 🚀 Project Overview

The system implements a human-in-the-loop AI trading workflow:

```text
User
 │
 ▼
FastAPI
 │
 ▼
Create Trade Request
 │
 ▼
Fetch Market Data
 │
 ▼
LLM Market Analysis
 │
 ▼
Generate Trade Proposal
 │
 ▼
Human Approval
 │
 ├─────────────── Reject ───────► END
 │
 ▼
Execute Trade
 │
 ▼
Execution Result
```

The workflow is implemented using **LangGraph**, allowing the application to maintain state and pause execution for human approval.

---

## 🏗️ Project Structure

```text
AI-Trading-Agent/
│
├── main.py
│
└── app/
    │
    ├── api/
    │   ├── __init__.py
    │   └── trading.py
    │
    ├── graph/
    │   ├── nodes.py
    │   ├── state.py
    │   └── workflow.py
    │
    ├── schemas/
    │   ├── approval_schema.py
    │   ├── order_schema.py
    │   └── trade_schema.py
    │
    └── services/
        ├── broker.py
        ├── llm.py
        └── market_data.py
```

### File Responsibilities

| File                         | Responsibility                                                    |
| ---------------------------- | ----------------------------------------------------------------- |
| `main.py`                    | FastAPI application entry point and PostgreSQL checkpointer setup |
| `api/__init__.py`            | Creates the application router and registers trading routes       |
| `api/trading.py`             | REST APIs for creating and approving trades                       |
| `graph/nodes.py`             | LangGraph nodes for market data, analysis, approval and execution |
| `graph/state.py`             | Defines the shared `TradingState`                                 |
| `graph/workflow.py`          | Builds and compiles the LangGraph workflow                        |
| `schemas/trade_schema.py`    | Validates incoming trade requests                                 |
| `schemas/approval_schema.py` | Validates human approval requests                                 |
| `schemas/order_schema.py`    | Defines the order structure                                       |
| `services/market_data.py`    | Provides simulated market data                                    |
| `services/llm.py`            | Configures the Groq LLM                                           |
| `services/broker.py`         | Simulates trade execution                                         |

---

## 🔄 Workflow

### 1. Submit Trade

The client sends a trade request containing:

```json
{
  "user_id": "user123",
  "symbol": "AAPL",
  "quantity": 10,
  "action": "BUY"
}
```

The API creates a unique `trade_id` that is also used as the LangGraph thread ID.

---

### 2. Market Data

The workflow retrieves simulated market information for the requested stock.

The current implementation generates:

* Current price
* Previous close
* Trading volume

The market-data service is intentionally simulated using randomly generated values.

---

### 3. AI Market Analysis

The LLM receives the requested trade and the supplied market data.

It is instructed to:

* Analyze the supplied market data
* Provide a concise analysis
* Determine whether the proposed trade appears reasonable based on the supplied data
* Avoid claiming certainty
* Avoid executing the trade

The analysis is then stored in the graph state and used to create a **trade proposal**.

---

### 4. Human-in-the-Loop Approval

Before execution, the workflow pauses using LangGraph's `interrupt()` mechanism.

The user receives the trade proposal and must explicitly approve or reject it.

```text
Trade Proposal
      │
      ▼
Human Review
      │
   ┌──┴──┐
   │     │
Approve Reject
   │     │
   ▼     ▼
Execute END
```

This prevents the LLM from directly executing a trade without human confirmation.

---

### 5. Trade Execution

If the user approves the proposal, the workflow creates an order containing:

```text
user_id
symbol
action
quantity
price
```

The broker service currently simulates execution and generates an order ID.

---

## 🧠 LangGraph Architecture

The graph consists of the following nodes:

```text
START
  │
  ▼
market_data
  │
  ▼
analyze_market
  │
  ▼
human_approval
  │
  ├──── rejected ────► END
  │
  ▼
execute_trade
  │
  ▼
 END
```

The workflow is defined using `StateGraph` and compiled with a PostgreSQL checkpointer.

The shared state contains fields such as:

```text
user_id
symbol
quantity
action
market_data
analysis
trade_proposal
approved
execution_result
```

This state is defined using a `TypedDict`.

---

## 🔌 API Endpoints

### Create Trade

```http
POST /trades
```

Example request:

```json
{
  "user_id": "user123",
  "symbol": "AAPL",
  "quantity": 10,
  "action": "BUY"
}
```

The API returns a trade ID, proposal and interruption information while waiting for approval.

---

### Approve / Reject Trade

```http
POST /trades/{trade_id}/approval
```

Approve:

```json
{
  "approved": true
}
```

Reject:

```json
{
  "approved": false
}
```

The approval endpoint resumes the interrupted LangGraph execution using the trade's `thread_id`.

---

## 🛠️ Tech Stack

### Backend

* Python
* FastAPI
* Pydantic

### Agentic AI

* LangGraph
* LangChain
* Groq LLM

### Database / Persistence

* PostgreSQL
* LangGraph PostgreSQL Checkpointer

### Architecture Concepts

* Agentic workflow
* State-based orchestration
* Human-in-the-loop
* Conditional routing
* LLM-based decision support
* API-driven architecture
* Persistent workflow state

---

## 🔐 Configuration

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=your_groq_model
DATABASE_URL=your_postgresql_connection_string
```

The application loads the database URL from the environment and raises an error if it is missing.

The LLM configuration uses `ChatGroq` with temperature set to `0`.

---

## ▶️ Running the Project

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd AI-Trading-Agent
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create `.env`:

```env
GROQ_API_KEY=your_api_key
GROQ_MODEL=your_model
DATABASE_URL=your_postgresql_url
```

### 5. Start the application

```bash
uvicorn main:app --reload
```

The FastAPI application initializes the PostgreSQL checkpointer during its lifespan and builds the LangGraph workflow.

---

## 📚 What I Learned

This project helped me understand and implement several concepts relevant to **Agentic AI engineering**:

* Designing stateful agent workflows
* Building workflows with LangGraph
* Implementing human-in-the-loop interactions
* Using conditional edges for workflow routing
* Managing state across multiple workflow steps
* Integrating an LLM into an application workflow
* Designing FastAPI endpoints around an agent workflow
* Using PostgreSQL for workflow checkpoint persistence
* Separating API, workflow, schema and service layers
* Designing an application where an LLM provides **decision support rather than direct execution**

---

## 🔮 Future Improvements

Possible improvements for future versions:

* Connect to a real market-data provider
* Integrate a paper-trading brokerage API
* Add authentication and authorization
* Add portfolio and position management
* Add risk-management rules
* Add transaction history
* Add structured LLM outputs
* Add automated evaluation of LLM analysis
* Add logging and observability
* Add unit and integration tests
* Add Docker deployment
* Add retry and failure-handling mechanisms
* Add rate limiting and API security
* Add asynchronous/background workflow execution

---

## ⚠️ Disclaimer

This project is intended for **educational and demonstration purposes only**.

The current implementation uses simulated market data and simulated trade execution. It is not financial advice and should not be used for real-world trading without substantial additional engineering, validation, security controls and regulatory considerations.

---

## 👨‍💻 Author

**Gunja**

Interested in **Generative AI, Agentic AI, LLM applications and backend engineering**.

This project was built to explore how AI agents can be integrated with backend systems and controlled workflows using modern AI engineering patterns.
