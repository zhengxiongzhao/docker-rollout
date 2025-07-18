# Flask Example Project

This is a basic Flask example project that includes a health check endpoint, a basic API endpoint, XXL-Job integration, Prometheus monitoring, and logging.

## Project Structure

```
flask-example/
├── src/
│   └── app.py       # Flask application code
├── Dockerfile       # Dockerfile
├── requirements.txt # Dependency management file
└── README.md        # Project documentation
```

## Configuration

The application is configured using environment variables. The following environment variables are supported:

* `API_KEY`: The API key to use for the application.

## Running the Application

To run the application, you need to have Docker installed.

1. Run Python Command Ci

   ```
   python src/app.py
   # OR
   PYTHONPATH=src gunicorn -c src/gunicorn.conf.py src.app:app
   ```
2. Run the Docker container:

   ```
   # Build the Docker image
   docker build -t flask-example:latest ./flask-example --load

   # Run the Docker container
   docker run -d -p 5000:5000 -p 9999:9999 flask-example:latest
   ```

## Testing the Application

To test the application, you can use the following commands:

1. Test the health check endpoint:

```bash
curl http://localhost:8000/health
```

2. Test the API endpoint:

```bash
curl http://localhost:8000/api/example
```

3. Test the XXL-Job callback endpoint:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"job_id": 1, "job_status": "success"}' http://localhost:8000/xxl-job-callback
```

4. View the Prometheus metrics:

```bash
curl http://localhost:8000/metrics
```

## Logging

The application uses the Python logging module for logging. The logs are written to the console. You can configure the logging level using the LOG_LEVEL environment variable.

## Unit Tests

This project does not include unit tests.

## CI/CD Configuration

This project does not include CI/CD configuration.
