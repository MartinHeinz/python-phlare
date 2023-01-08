FROM python:3.10

COPY requirements.txt .
COPY app.py .

RUN pip install -r requirements.txt

EXPOSE 8080
CMD python3 -u app.py

# docker build -t python-phlare -f python.Dockerfile .
# docker run -p 8080:8080 -e INSTANCE=low -e CPU_LOAD=500 -e MEMORY_LOAD=500 -e LOAD_TYPE="MEMORY" --name python-phlare --rm python-phlare
# ...
# Starting service instance: low
# Data was allocated, sleeping...
# 10.244.0.14 - - [08/Jan/2023 11:00:39] "GET /debug/pprof/profile?seconds=14 HTTP/1.1" 200 -
# 10.244.0.14 - - [08/Jan/2023 11:00:39] "GET /debug/pprof/heap HTTP/1.1" 200 -
# ...