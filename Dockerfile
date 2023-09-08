FROM python:3.9.7

WORKDIR /usr/src/app

COPY requirements.txt ./

RUN  pip install --no-cache-dir -r requirements.txt

#Copy current working directory to docker workdir

COPY . .

CMD ["uvicorn", "main:app", "--host", "127.0.0.1", "--port", "8000"]

