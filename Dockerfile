FROM python:3.9

RUN mkdir /fabric_defect_api

COPY . /fabric_defect_api

WORKDIR /fabric_defect_api

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]