#!/bin/bash

# 函数：测试 HTTP 端点
test_http() {
    URL="http://127.0.0.1:5001/health"
    echo "Testing HTTP endpoint: $URL"
    for i in $(seq 1 120); do
      curl -o /dev/null -s -w "$(date +'%Y-%m-%d %H:%M:%S.%3N') - %{http_code}\n" "$URL"
      sleep 1
    done
}

# 函数：测试 TCP 连接 (通过 curl 实现)
test_tcp() {
    HOST="localhost"
    PORT="9999"
    echo "Testing TCP (via HTTP GET) on: $HOST:$PORT"
    for i in $(seq 1 120); do
      # if curl -v --connect-timeout 2 telnet://"$HOST":"$PORT" 2>&1 | grep -q "Connected"; then
      # if nc -zv -w 1 $HOST $PORT >/dev/null 2>&1; then
      #   echo "$(date +'%Y-%m-%d %H:%M:%S.%3N') - Port $PORT on $HOST is OPEN."
      # else
      #   echo "$(date +'%Y-%m-%d %H:%M:%S.%3N') - Port $PORT on $HOST is CLOSED."
      # fi
        curl -o /dev/null -s -w "$(date +'%Y-%m-%d %H:%M:%S.%3N') - %{http_code}\n" --connect-timeout 2 "http://$HOST:$PORT"
        sleep 1
    done
}

# 主逻辑：根据第一个参数选择执行的函数
if [ "$1" == "tcp" ]; then
    test_tcp
elif [ "$1" == "http" ]; then
    test_http
else
    echo "Usage: $0 {tcp|http}"
    exit 1
fi
