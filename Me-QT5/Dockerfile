FROM --platform=amd64 ubuntu:18.04

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip

WORKDIR /workspace
COPY ./final_pipeline ./final_pipeline

COPY ./setup.sh ./final_pipeline/setup.sh
COPY ./run.sh ./final_pipeline/run.sh
RUN chmod +x ./final_pipeline/setup.sh
RUN chmod +x ./final_pipeline/run.sh

RUN ./final_pipeline/setup.sh

CMD ["./run.sh"]
EXPOSE 8501