# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory in the container
WORKDIR /weather_app

# Copy the requirements file and install dependencies
COPY weather_app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 5000 for the Flask app
EXPOSE 5000

# Define the default command to run the Flask app
CMD ["python", "app.py"]
