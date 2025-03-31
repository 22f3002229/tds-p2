# FastAPI Project

This is a FastAPI project that provides an API endpoint for submitting questions along with optional file attachments. The application processes the incoming data and returns a JSON response containing an answer.

## Project Structure

```
fastapi-project
├── app
│   ├── main.py               # Entry point of the FastAPI application
│   ├── api
│   │   └── endpoints
│   │       └── question.py   # API endpoint for handling questions
│   └── models
│       └── __init__.py       # Data models or schemas (currently empty)
├── requirements.txt          # Project dependencies
└── README.md                 # Project documentation
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd fastapi-project
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the dependencies:**
   ```
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```
   uvicorn app.main:app --reload
   ```

## Usage

To use the API, send a POST request to the `/api/question` endpoint with `multipart/form-data` containing a `question` field and optionally attach files.

### Example Request

```
POST /api/question
Content-Type: multipart/form-data

{
  "question": "What is the capital of France?",
  "files": [<file1>, <file2>]
}
```

### Example Response

```json
{
  "answer": "The capital of France is Paris."
}
```

## License

This project is licensed under the MIT License.