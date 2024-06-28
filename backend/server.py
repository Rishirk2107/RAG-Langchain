import logging
import os
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
import Worker_completed as worker  # Import the worker module
from supabase import create_client, Client

# Initialize FastAPI app and CORS
app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Ensure the uploads directory exists
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

templates = Jinja2Templates(directory="/backend/templates")

# Supabase configuration
SUPABASE_URL = "https://dpcxsrewkypifzmdqvsf.supabase.co/storage/v1/s3"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImRwY3hzcmV3a3lwaWZ6bWRxdnNmIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTcxODg5ODE5OSwiZXhwIjoyMDM0NDc0MTk5fQ.X4U0WeodvKRJV9oeH2zlAw0YmGfWghAuI5icCHgCOqw"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Define the route for the index page
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Define the route for processing messages
@app.post("/process-message")
async def process_message_route(userMessage: str = Form(...)):
    logger.debug(f"user_message: {userMessage}")

    if not userMessage:
        raise HTTPException(status_code=400, detail="Please provide a message to process.")

    try:
        bot_response = worker.process_prompt(userMessage)  # Process the user's message using the worker module
        return JSONResponse(content={"botResponse": bot_response}, status_code=200)
    except Exception as e:
        logger.error(f"Error processing message: {e}")
        raise HTTPException(status_code=500, detail="There was an error processing your message.")

# Define the route for processing documents
@app.post("/process-document")
async def process_document_route(file: UploadFile = File(...)):
    if file.filename == '':
        raise HTTPException(status_code=400, detail="No file selected. Please try again.")

    # Define the path where the file will be saved in the uploads directory
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    try:
        logger.debug(f"Saving file to {file_path}")
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())
        logger.debug(f"File saved successfully to {file_path}")

        worker.process_document(file_path)  # Process the document using the worker module

        return JSONResponse(content={
            "botResponse": "Thank you for providing your PDF document. I have analyzed it, so now you can ask me any "
                           "questions regarding it!"
        }, status_code=200)
    except Exception as e:
        logger.error(f"Error saving or processing document: {e}")
        raise HTTPException(status_code=500, detail="There was an error processing your document.")

# Define the route for downloading a file from Supabase bucket storage
@app.get("/download/{file_name}")
async def download_file(file_name: str):
    try:
        # Download the file from the Supabase bucket
        response = supabase.storage.from_("docs").download(file_name).data
        print(response.status_code)
        
        if not response:
            raise HTTPException(status_code=404, detail="File not found in Supabase bucket.")

        # Define the path where the file will be saved in the uploads directory
        file_path = os.path.join(UPLOAD_FOLDER, file_name)

        # Save the downloaded file to the uploads directory
        with open(file_path, "wb") as file:
            file.write(response.content)
        
        return JSONResponse(content={
            "message": f"File {file_name} downloaded successfully and saved to {UPLOAD_FOLDER}."
        }, status_code=200)
    except Exception as e:
        logger.error(f"Error downloading file from Supabase: {e}")
        raise HTTPException(status_code=500, detail="There was an error downloading the file.")

# Run the FastAPI app using Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="debug")
