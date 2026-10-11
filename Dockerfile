FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir pandas matplotlib

COPY data/raw/stix_flares.csv data/raw/stix_flares.csv
COPY generated_code/zero_shot_01.py generated_code/zero_shot_01.py

CMD ["python", "generated_code/zero_shot_01.py"]