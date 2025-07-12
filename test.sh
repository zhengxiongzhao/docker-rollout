URL=http://127.0.0.1:5001/health
for i in $(seq 1 120); do
  curl -o /dev/null -s -w "$(date +'%Y-%m-%d %H:%M:%S.%3N') - %{http_code}\n" "$URL"
  sleep 1 # 等待1秒
done
