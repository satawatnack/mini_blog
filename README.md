# Mini blog (flask app)
CRUD for Mini blog with author name authentication

## Project setup

1. create your env file and add 
2. run db
```
cd postgres
docker compose up -d
```
3. create blog schema in your postgres db
4. install dependencies
```
cd mini_blog
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```
5. run app
```
python3 src/main.py
```