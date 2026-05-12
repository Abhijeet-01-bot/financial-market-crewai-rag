# Financial Market Intelligence CrewAI RAG System

A multi-agent financial market intelligence application built using **CrewAI**, **RAG**, **FAISS**, **HuggingFace Embeddings**, **Gemini LLM**, **FastAPI**, **Streamlit**, **Docker**, and **GitHub Actions**.

This project implements an agentic Retrieval-Augmented Generation workflow for analyzing financial market data, sector outlook, risk exposure, and educational portfolio allocation.

---

## Project Overview

The goal of this project is to build an end-to-end **Financial Market Intelligence Assistant** that can:

- Retrieve relevant financial market information from a vector database.
- Analyze market and sector outlook.
- Assess portfolio and sector risk.
- Generate educational portfolio allocation suggestions.
- Expose the system through a REST API using FastAPI.
- Provide an interactive Streamlit chat interface.
- Support Docker-based deployment and CI/CD automation.

---

## Key Features

- Web-sourced financial data collection using `yfinance`
- Text corpus preparation from financial market data
- FAISS vector database for semantic search
- HuggingFace embeddings using `sentence-transformers/all-MiniLM-L6-v2`
- CrewAI-based multi-agent workflow
- RAG implemented as a callable CrewAI tool
- FastAPI backend with `/query` endpoint
- Streamlit chat-style frontend
- Dockerfile and Docker Compose deployment
- Unit testing with Pytest
- GitHub Actions CI/CD workflow
- Evaluation using BLEU, ROUGE, and relevance score
- Baseline RAG vs Agentic CrewAI RAG comparison
- Feedback and retraining trigger support

---

## Architecture

```text
User Query
   |
   v
Streamlit UI
   |
   v
FastAPI /query Endpoint
   |
   v
CrewAI Multi-Agent Workflow
   |
   +--> Retriever Agent
   |       |
   |       v
   |   Financial RAG Search Tool
   |       |
   |       v
   |   FAISS Vector Store
   |
   +--> Market Analysis Agent
   |
   +--> Risk Assessment Agent
   |
   +--> Portfolio Allocation Agent
   |
   v
Final Educational Financial Intelligence Response

---

## Project Structure

financial-market-crewai-rag/
│
├── api/
│   ├── __init__.py
│   ├── app.py
│   └── schemas.py
│
├── crew/
│   ├── __init__.py
│   ├── agents.py
│   ├── crew_runner.py
│   ├── tasks.py
│   └── tools.py
│
├── data/
│   ├── raw/
│   │   ├── market_reports.txt
│   │   ├── stock_news.txt
│   │   ├── historical_data.txt
│   │   ├── sector_outlook.txt
│   │   └── risk_commentary.txt
│   └── processed/
│
├── feedback/
│
├── saved_outputs/
│   └── agentic_answer_1.txt
│
├── src/
│   ├── __init__.py
│   ├── baseline_rag.py
│   ├── data_loader.py
│   ├── evaluation.py
│   ├── evaluation_offline.py
│   ├── feedback.py
│   ├── fetch_web_financial_data.py
│   ├── hybrid_retriever.py
│   ├── rag_pipeline.py
│   ├── retrieval_validation.py
│   ├── retraining_trigger.py
│   └── vector_store.py
│
├── streamlit_app/
│   ├── main.py
│   └── test.py
│
├── tests/
│   ├── test_api.py
│   └── test_retriever.py
│
├── vectorstore/
│   └── faiss_index/
│       ├── index.faiss
│       └── index.pkl
│
├── .github/
│   └── workflows/
│       └── ci_cd.yml
│
├── .dockerignore
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── requirements_docker.txt
├── requirements_freeze.txt
└── README.md

---







