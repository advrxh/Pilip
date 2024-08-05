FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 5656:5656

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5656"]