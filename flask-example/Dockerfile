FROM python:3.9-slim-buster AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

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

# 从 builder 阶段复制安装好的依赖
COPY --from=builder /root/.local /root/.local
# 复制应用代码
COPY src/ .
COPY application.yaml .

# 确保 Python 能找到安装的包
ENV PATH=/root/.local/bin:$PATH

EXPOSE 5000
EXPOSE 9999

# CMD ["python", "app.py"]
CMD ["gunicorn", "-c", "gunicorn.conf.py", "app:app"]
