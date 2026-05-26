This is a CRUD API created from scratch using Python, FastAPI and Pydantic

Project is a simple to do list i created just to get used to how FastAPI works

Added Auth with JWT tokens and password hashing with bcrypt
Also protected endpoints

Added a database using SQLite and SQLAlchemy for data persistence
When creating database tables i kept normalization in mind with a users and tasks table linked by a foreign key

Containerized the app with Docker and deployed to AWS ECS using ECR to store the image
Live on AWS Fargate at http://13.50.108.179:8000/docs (i have most likely turned it offline to avoid charges)

To run clone repo, create virtual environment, install dependencies and run the server