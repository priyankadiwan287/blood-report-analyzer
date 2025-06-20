from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from app.file_handler import extract_text_from_pdf, extract_text_from_image
from app.llm_predictor import analyze_report

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def home():
    return """
    <h2>🩺 Upload Blood Report</h2>
    <form action="/analyze" enctype="multipart/form-data" method="post">
      <input name="file" type="file">
      <input type="submit">
    </form>
    """

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):
    if file.filename.endswith(".pdf"):
        text = extract_text_from_pdf(file)
    else:
        text = extract_text_from_image(file)
    result = analyze_report(text)
    return {"result": result}
