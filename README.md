# PurpleMerit War Room - Multi-Agent Launch Decision System


A multi-agent system that simulates a cross-functional war room for product launch decisions. The system analyzes metrics and user feedback to produce a structured decision: **Proceed / Pause / Roll Back**.

##  Overview

This project replicates a real-world product launch scenario where multiple teams collaborate to make critical decisions under uncertainty. It brings together different perspectives through autonomous agents that mimic key roles in an organization.

The system processes:
- Time-series product metrics (e.g., DAU, retention, crash rate, etc.)
- User feedback (positive, neutral, and negative sentiments)
- Release notes and known issues

Based on these inputs, the system generates a well-structured decision along with actionable insights.

## Key Features

-  Multi-agent architecture with clearly defined responsibilities  
-  Orchestrator to coordinate agent interactions and workflow  
-  Tool-based analysis (metric trends, anomaly detection, sentiment analysis)  
-  Structured output in JSON format for decision-making  
-  Transparent logs for traceability of each step  

##  Agents Involved

- **Product Manager Agent** – Defines success criteria and makes the final decision framing  
- **Data Analyst Agent** – Analyzes metrics, detects trends and anomalies  
- **Marketing/Comms Agent** – Evaluates user sentiment and communication impact  
- **Risk/Critic Agent** – Identifies risks, challenges assumptions, and ensures robustness  

##  Objective

To simulate collaborative decision-making in a high-stakes environment and provide a clear, data-driven recommendation with:
- Decision (Proceed / Pause / Roll Back)
- Rationale based on metrics and feedback
- Risk register and mitigation strategies
- Action plan for the next 24–48 hours
- Communication strategy
- Confidence score

## Architecture
