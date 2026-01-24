# Command for installing backend dependencies through uv

    uv add "fastapi[all]" langchain langchain-openai python-dotenv sqlalchemy uvicorn psycopg2-binary

## Command for installing frontend

    npm create vite@latest frontend -- --template react
    cd frontend
    npm install
    npm install axios
