# tools-app
FastAPI backend and Streamlit frontend for tool site apps

## Backend Setup (FastAPI)

1. Navigate to the `fastapi-app` directory:
   ```
   cd fastapi-app
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS and Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Running the Backend

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

## Frontend Setup (Streamlit)

1. Navigate to the `streamlit-app` directory:
   ```
   cd streamlit-app
   ```

2. Create a virtual environment (if not already created):
   ```
   python -m venv venv
   ```

3. Activate the virtual environment (if not already activated).

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Running the Frontend

1. Make sure your virtual environment is activated.

2. Set the FastAPI endpoint environment variable (if needed):
   - On Windows:
     ```
     set FASTAPI_ENDPOINT=http://localhost:8000
     ```
   - On macOS and Linux:
     ```
     export FASTAPI_ENDPOINT=http://localhost:8000
     ```

3. Run the Streamlit application:
   ```
   streamlit run streamlit_app.py
   ```

4. The Streamlit app will be available at `http://localhost:8501`.
