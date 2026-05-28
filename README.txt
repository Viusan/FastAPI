This is a CRUD API created from scratch using Python, FastAPI and Pydantic

Project is a simple to do list i created just to get used to how FastAPI works

Added Auth with JWT tokens and password hashing with bcrypt
Also protected endpoints

Added a database using SQLite and SQLAlchemy for data persistence, also i have now added postgreSQL support
When creating database tables i kept normalization in mind with a users and tasks table linked by a foreign key

Containerized the app with Docker and deployed to AWS ECS using ECR to store the image, and added docker compose yml file.
Live on AWS Fargate at http://13.50.108.179:8000/docs (i have most likely turned it offline to avoid charges)

I added nginx which creates a reverse proxy layer infront of API. 
Now all traffic goes through nginx first instead of directly going to fastapi.


To run clone repo, create virtual environment, install dependencies and run the server

What was learnt from this simple project was how FASTApi works and genrelly api and methods.
Basic backend security like tokens and hashing.
About how dockerfiles, images and containers work. Why its more efficient to use Docker.
Added reverse proxy layer with nginx, why its key for saftey.
Used docker compose yml file to run multiple containers.
How to set up AWS and very basic cloud deployment works with this project.
How ECR is storage for images in cloud, and ECS is what actually runs container on AWS infrastructure.
