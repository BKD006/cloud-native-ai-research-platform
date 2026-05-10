from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse
from src.api.services.report_services import ReportService

router = APIRouter()
service = ReportService()

# Direct dashboard access
@router.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return request.app.templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={
            "request": request,
            "user": "Guest"
        }
    )


@router.post("/generate_report", response_class=HTMLResponse)
async def generate_report(request: Request, topic: str = Form(...)):
    # service = ReportService()

    result = service.start_report_generation(topic, 3)
    thread_id = result["thread_id"]

    return request.app.templates.TemplateResponse(
        request=request,
        name="reportprogress.html",
        context={
            "request": request,
            "topic": topic,
            "feedback": "",
            "thread_id": thread_id,
        }
    )


@router.post("/submit_feedback", response_class=HTMLResponse)
async def submit_feedback(
    request: Request,
    topic: str = Form(...),
    feedback: str = Form(...),
    thread_id: str = Form(...),
):
    # service = ReportService()

    print("STEP 1")
    service.submit_feedback(thread_id, feedback)
    print("STEP 2")
    result = service.get_report_status(thread_id)
    print("STEP 3")
    doc_path = result.get("docx_path")
    pdf_path = result.get("pdf_path")

    return request.app.templates.TemplateResponse(
        request=request,
        name="reportprogress.html",
        context={
            "request": request,
            "topic": topic,
            "feedback": feedback,
            "doc_path": doc_path,
            "pdf_path": pdf_path,
            "thread_id": thread_id,
        }
    )


@router.get("/download/{file_name}", response_class=HTMLResponse)
async def download_report(file_name: str):
    # service = ReportService()

    file_response = service.download_file(file_name)

    if file_response:
        return file_response

    return {"error": f"File {file_name} not found."}