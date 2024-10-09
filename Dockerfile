# Use the full Python image
FROM python:3.10

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Install pipenv
RUN pip3 install pipenv

# Copy the Pipfile and Pipfile.lock
COPY Pipfile Pipfile.lock /app/

# Install dependencies
RUN pipenv install --system --deploy

# Copy the rest of your application code
COPY . /app

# Expose port 8000 for the Django development server
EXPOSE 8000

# Command to run the development server
CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]
