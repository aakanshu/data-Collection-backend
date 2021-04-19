FROM python:3.9-slim

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x start.sh
ENV FLASK_ENV=dev
EXPOSE 5000
CMD ./start.sh
