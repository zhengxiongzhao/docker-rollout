```bash
# Create directory for Docker cli plugins
mkdir -p ~/.docker/cli-plugins

# Download docker-rollout script to Docker cli plugins directory
curl https://raw.githubusercontent.com/wowu/docker-rollout/main/docker-rollout -o ~/.docker/cli-plugins/docker-rollout

# Make the script executable
chmod +x ~/.docker/cli-plugins/docker-rollout
```


```bash
docker build -t flask-example:latest ./flask-example --load
docker run -d -p 5000:5000 -p 9999:9999 flask-example:latest
```


```bash
docker rollout api_server
```
