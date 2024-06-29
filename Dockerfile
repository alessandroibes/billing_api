FROM python:3.9-slim

WORKDIR /app

#COPY ./src /src

#COPY ./src/dependencies/requirements.txt /app/requirements.txt
COPY src/dependencies/requirements.txt requirements.txt
COPY src/dependencies/requirements-dev.txt requirements-dev.txt

#RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
RUN pip install --no-cache-dir -r requirements-dev.txt

#COPY ./src /app/src
COPY src /app/src

ENV PYTHONPATH=/app/src

#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]