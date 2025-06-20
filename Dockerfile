FROM python:3.10-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Ensure static directory exists
RUN mkdir -p static

# Expose the port for the MCP server
# Note: Hugging Face Spaces will set the PORT environment variable
EXPOSE 7860

# Run the FastMCP server
CMD ["python", "main.py"]
