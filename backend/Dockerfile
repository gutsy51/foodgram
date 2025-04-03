FROM python:3.13.2-alpine

WORKDIR /app/

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt --no-cache-dir

COPY . .

CMD ["gunicorn", "--bind", "0:8000", "--chdir", "foodgram", "foodgram.wsgi:application"]