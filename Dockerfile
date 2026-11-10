FROM python:3.12-slim
WORKDIR /app
COPY app.py sample_demand.csv ./
USER 10001:10001
EXPOSE 8080
CMD ["python", "-B", "app.py", "--host", "0.0.0.0"]
