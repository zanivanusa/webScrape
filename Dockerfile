# Use an official Python runtime as the base image
FROM python:3.9

# Set the working directory in the container to /app
WORKDIR /app

#installing the dependencies we used
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /app
COPY . /app


# Make port 8080 available to the world outside this container
EXPOSE 8080

# Define the command to run your app using CMD which keeps the container running
CMD ["python", "server.py"]
