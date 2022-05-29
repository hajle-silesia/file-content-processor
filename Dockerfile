FROM python:3.9
RUN apt update && apt install -y \
    curl
WORKDIR project
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY ./src ./src
ENV PYTHONPATH "${PYTHONPATH}:/project"
ENTRYPOINT ["python", "src/main.py"]
