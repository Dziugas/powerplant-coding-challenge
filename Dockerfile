FROM python:3.12-alpine

# Set environment variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Expose port
EXPOSE 8888

# Create and set the working directory
WORKDIR /app

# Copy only the requirements file initially
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Remove the requirements file
RUN rm requirements.txt

# Copy the entire application code
COPY . .

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod a+x /entrypoint.sh

# Specify the entrypoint command
ENTRYPOINT ["/entrypoint.sh"]