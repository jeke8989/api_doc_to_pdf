from fastapi import FastAPI, UploadFile, HTTPException, File, Form, BackgroundTasks
from fastapi.responses import FileResponse
from typing import Dict, Optional
from pydantic import BaseModel
import core, json, os, logging
from docx.document import Document as DocumentObject



app = FastAPI()
logging.basicConfig(level=logging.INFO)

def delete_file(path: str):
    try:
        os.remove(path)
    except Exception as e:
        print(f"Error deleting file {path}: {e}")


@app.post('/update_doc', description='Upload file', name="hello 2")
async def hello(file: UploadFile, update_dict: str, add_rows: str, back_tasks: BackgroundTasks ) -> FileResponse:
    update_data = {}
    rows_data = []
    if update_dict:
        try:
            # Парсим JSON строку в словарь
            update_data = json.loads(update_dict)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail='Invalid JSON format in update_dict')
    if add_rows:
        try:
            # Парсим JSON строку в словарь
            rows_data = json.loads(add_rows)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail='Invalid JSON format in update_dict')
    print(rows_data)
    document = await core.get_doc_file(file=file)
    file_pdf_name = core.replace_data(replacements=update_data, doc=document, add_rows=rows_data)
    back_tasks.add_task(delete_file, file_pdf_name)
    back_tasks.add_task(delete_file, 'amendment3.docx')
    return FileResponse(file_pdf_name, media_type='application/pdf', filename=file_pdf_name)