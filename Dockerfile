# Use official Python image 

FROM python:3.9-slim 

 

# Set working directory 

WORKDIR /app 

# Copy files 

COPY . /app 

 

# Install dependencies 

RUN pip install --no-cache-dir -r requirements.txt 


EXPOSE 5000 

 

# Run the app 

CMD ["python", "app.py"] 