FROM python:3.10

ENV PYTHONDONTWRITEBYTECIDE 1
ENV PYTHONBUFFERED 1

RUN pip install --upgrade pip

WORKDIR /todo-backend

COPY ./requirements.txt /todo-backend/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /todo-backend/requirements.txt

COPY . /todo-backend

CMD ["uvicorn", "main:app", "--port", "8000", "--host", "0.0.0.0"]
