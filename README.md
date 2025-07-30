# Wit Content Generation API

Production API server for generating trivia questions and daily challenges for the Wit cognitive game.

## 🚀 Quick Deploy

This repository is configured for automatic deployment on Railway.

## 📡 API Endpoints

- `GET /health` - Health check
- `POST /generate-questions` - Generate domain questions
- `POST /generate-daily-challenge` - Generate daily challenge
- `POST /generate-bulk-questions` - Generate 10k questions
- `POST /generate-daily-challenges-bulk` - Generate 2 years of challenges
- `POST /validate` - Validate questions

## 🔧 Usage

Deploy to Railway and use the provided URL in your n8n workflows.

## 📦 Dependencies

- Flask
- Flask-CORS
- Python 3.8+ 