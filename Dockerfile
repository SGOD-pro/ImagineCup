FROM python:3.11-slim

RUN useradd -m myuser

WORKDIR /app


COPY requirements.txt requirements.txt
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

COPY . .
RUN chown -R appuser:myuser /app

USER myuser

EXPOSE 8000
CMD [ "uvicorn", "main:app" , "--host", "0.0.0.0", "--port", "8000" ]