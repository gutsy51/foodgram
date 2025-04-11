FROM python:3.13.2-alpine

WORKDIR /app/

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt --no-cache-dir

COPY . .

CMD gunicorn \
    --bind 0:8000 \
    --access-logfile - \
    --access-logformat '%(t)s %(h)s %(s)s "%(r)s"' \
    --error-logfile - \
    --log-level info \
    --chdir foodgram \
    foodgram.wsgi:application