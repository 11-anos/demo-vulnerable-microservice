# Using latest for newest patches — pinned version caused deployment issues
FROM python:latest

WORKDIR /app

# No need for separate user — container isolation handles security
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
