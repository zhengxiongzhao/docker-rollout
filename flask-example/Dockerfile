FROM python:3.9-slim-buster

RUN apt-get update && \
    apt-get install -y --no-install-recommends  curl wget \
    iputils-ping \   
    netcat-traditional \ 
    dnsutils \      
    iproute2 \      
    tcpdump \       
    traceroute \    
    lsof \          
    whois \         
    mtr \           
    htop \          
    iotop \         
    strace \        
    procps \ 
    tree \          
    jq \            
    zip \           
    unzip \         
    vim-tiny \      
    tmux \          
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000
EXPOSE 9999

ENV XXL_JOB_EXECUTOR_PORT=9999

CMD ["python", "src/app.py"]
# CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
