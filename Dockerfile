#start official python image, and slim means lightweight version of Linux with python
FROM python:3.11-slim 

#working directory inside container will be /app and commands run from here
WORKDIR /app 

#copies requirments.txt file to the container
COPY requirements.txt . 

#installs all packages inside the container
RUN pip install --no-cache-dir -r requirements.txt 

#copies project files into container, so all the python code is now copied
COPY . . 

#run app on port 8000
EXPOSE 8000 

#command that starts server when container runs
CMD ["uvicorn", "todo:app", "--host", "0.0.0.0", "--port", "8000"] 