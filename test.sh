URL=http://127.0.0.1:8082/cong/admin/login.html
for i in $(seq 1 60); do
  curl -o /dev/null -s -w "%{http_code}\n" "$URL"
  sleep 1 # 等待1秒
donels