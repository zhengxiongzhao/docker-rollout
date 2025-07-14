Docker Rollout

```bash
# Create directory for Docker cli plugins
mkdir -p ~/.docker/cli-plugins

# Download docker-rollout script to Docker cli plugins directory
curl https://raw.githubusercontent.com/wowu/docker-rollout/main/docker-rollout -o ~/.docker/cli-plugins/docker-rollout

# Make the script executable
chmod +x ~/.docker/cli-plugins/docker-rollout
```


```bash
# 初始化
docker build -t flask-example:latest ./flask-example --load
docker compose up -d && docker compose logs -f

# 滚动部署
docker build -t flask-example:latest ./flask-example --load
docker rollout api_server
```


Docker Swarm

```bash
# 初始化
docker swarm init
docker build -t flask-example:latest ./flask-example --load
docker stack deploy -c docker-compose-swarm.yaml flask-example

# 滚动部署
docker build -t flask-example:latest ./flask-example --load
docker service update --force --image flask-example:latest flask-example_api_server
```
