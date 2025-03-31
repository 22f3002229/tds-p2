from fastapi import APIRouter, File, UploadFile, Form
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/ask")
async def ask_question(question: str = Form(...), files: list[UploadFile] = File(None)):
    # Here you would process the question and files as needed
    answer = f"You asked: {question}"
    
    if files:
        file_names = [file.filename for file in files]
        answer += f" with attachments: {', '.join(file_names)}"
    
    return JSONResponse(content={"answer": answer})