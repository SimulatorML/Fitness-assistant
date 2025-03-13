# 🏗️ Fitness Assistant - Setup Guide

This guide explains how to run main components of the Fitness Assistant with poetry and test them.

---

## 📦 Installing Poetry  
Poetry is used for package management in this project. To install it:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

To verify the installation:
```bash
poetry --version
```

---

## 🛠️ Installing Dependencies  
After cloning the repository, install all dependencies using:

```bash
poetry install
```

This will set up a **virtual environment** and install all required packages.

---

## 🚀 Running the FastAPI Server  
To start the FastAPI application, use:

```bash
poetry run python -m api
```

#### 📌 **Checking the API in Swagger UI**  
Once the server is running, open your browser and go to:

- **Swagger Docs** → [http://0.0.0.0:8000/docs](http://127.0.0.1:8000/docs)


#### 🤖 Testing FastAPI with LLM Integration  
To test the FastAPI API with LLM integration, you must:
1. **Set up your `.env` file** with either `OPENAI_API_KEY` or `GOOGLE_API_KEY`.
2. **Define the LLM provider** in `llm/llm_config.py`:
   ```python
   llm_provider: "google"  # Options: google, openai
   ```
3. **Send a request to test the LLM endpoint (or use Swagger UI)**:
   ```http
   POST /api/v1/llm/request
   ```

Ensure your API keys are correct and that the selected LLM provider is available.



---

## 🤖 Running the Telegram Bot  
To start the Telegram bot, run:

```bash
poetry run python bot/__main__.py
```

#### 📌 **How to Test the Bot**  
1. Ensure your **Telegram Bot API token** is correctly set in `.env`. See `.env.example`.
2. Run the bot using the command above.
3. Open Telegram and **send `/start`** to your bot.

If the bot is running correctly, it should respond with a welcome message.

---

## 🧪 Running Tests  
To run all tests using `pytest`, execute:

```bash
poetry run python -m pytest
```

To test only the FastAPI API:
```bash
poetry run python -m pytest tests/test_api.py
```
---

## 🔄 Running Pre-Commit Hooks  
If you haven’t installed `pre-commit` yet, set it up with:

```bash
poetry run pre-commit install
```
Now, every time you commit, **tests and formatting checks will run automatically**.

---

## 📌 Summary of Commands  
| **Action** | **Command** |
|------------|------------|
| Install dependencies | `poetry install` |
| Run FastAPI | `poetry run python -m api` |
| Open API docs | [http://0.0.0.0:8000/docs](http://0.0.0.0:8000/docs) |
| Run Telegram bot | `poetry run python bot/__main__.py` |
| Run all tests | `poetry run python -m pytest` |
| Run only API tests | `poetry run python -m pytest tests/test_api.py` |
| Install pre-commit hooks | `poetry run pre-commit install` |

---