from fastapi import APIRouter, File, UploadFile, Form
from fastapi.responses import JSONResponse
import httpx
from typing import List
import subprocess

router = APIRouter()

@router.post("/ask")
async def ask_question(
    question: str = Form(...), 
    file: List[UploadFile] = File(None)
):
    # question += "*if a command have to executed then output should be 'command' in first line then followed by command in next line. Merge sequence of commands appropriately to form single line command. In Other cases, Only give final answer without any explanation or supporting statements.*"
    question += " *Only give final answer without any explanation or supporting statements.*"

    # Process uploaded files
    file_contents = []
    if file:
        for uploaded_file in file:
            content = await uploaded_file.read()  # Read file content
            file_contents.append({
                "filename": uploaded_file.filename,
                "content": content.decode("utf-8")  # Decode bytes to string
            })

    # Prepare the LLM API request
    llm_url = "http://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
    llm_headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJlbWFpbCI6IjIyZjMwMDIyMjlAZHMuc3R1ZHkuaWl0bS5hYy5pbiJ9.JM92BNZVhgls9ZRCsU7WQVhzKlDC5mSiCFyl7IGE23M"  # Replace with your actual token
    }

    # Add file content to the messages
    messages = [{"role": "user", "content": question}]
    for file_content in file_contents:
        messages.append({
            "role": "user",
            "content": f"File: {file_content['filename']}\nContent:\n{file_content['content']}"
        })

    llm_payload = {
        "model": "gpt-4o-mini",
        "messages": messages
    }

    # Forward the question to the LLM
    async with httpx.AsyncClient() as client:
        llm_response = await client.post(llm_url, json=llm_payload, headers=llm_headers)

    # Handle LLM response
    if llm_response.status_code == 200:
        llm_result = llm_response.json()
        llm_answer = llm_result.get("choices", [{}])[0].get("message", {}).get("content", "No response")
    else:
        llm_answer = f"Error: {llm_response.status_code} - {llm_response.text}"


    # Combine LLM answer with file information
    response = {
        "answer": llm_answer,
        # "uploaded_files": [file_content["filename"] for file_content in file_contents]
    }

    return JSONResponse(content=response)