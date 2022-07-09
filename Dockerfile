FROM python:3.10.5
RUN apt update && apt install -y \
    curl
WORKDIR project
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./src ./src
ENV PYTHONPATH "${PYTHONPATH}:/project"
ENTRYPOINT ["python", "src/main.py"]
