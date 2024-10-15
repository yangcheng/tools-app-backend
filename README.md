# tools-app-backend
fastapi based backend for tool site apps

## Setup

1. Create a virtual environment:
   ```
   python -m venv venv
   ```

2. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Running the Application

1. Make sure your virtual environment is activated.

2. Run the FastAPI application:
   ```
   python main.py
   ```

3. The API will be available at `http://localhost:8000`.

## API Endpoints

- `GET /`: Welcome message
- `POST /search`: Perform a search query

For more details on the API endpoints, refer to the FastAPI automatic documentation at `http://localhost:8000/docs` when the application is running.

