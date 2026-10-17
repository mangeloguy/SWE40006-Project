#!/usr/bin/env bash
set -euo pipefail

env_name="$1"
tag="$2"
app_dir="build-status-dashboard"

: "${DEPLOY_HOST:?DEPLOY_HOST is not set}"
: "${DEPLOY_USER:?DEPLOY_USER is not set}"
: "${DEPLOY_SSH_KEY:?DEPLOY_SSH_KEY is not set}"

if [[ ! "$env_name" =~ ^(staging|production)$ ]]; then
  echo "unknown environment: $env_name" >&2
  exit 1
fi

if [[ ! "$tag" =~ ^[0-9a-f]{7}$ ]]; then
  echo "invalid image tag: $tag" >&2
  exit 1
fi

mkdir -p ~/.ssh
printf '%s\n' "$DEPLOY_SSH_KEY" | tr -d '\r' > ~/.ssh/deploy_key
chmod 600 ~/.ssh/deploy_key
cat > ~/.ssh/config <<EOF
Host server
  HostName $DEPLOY_HOST
  User $DEPLOY_USER
  IdentityFile ~/.ssh/deploy_key
  StrictHostKeyChecking accept-new
  ConnectTimeout 15
EOF

ssh server "mkdir -p $app_dir"
scp "docker/compose.$env_name.yml" "server:$app_dir/compose.yml"

if [ -n "${GHCR_TOKEN:-}" ]; then

  AUTH=$(printf '%s:%s' "$GITHUB_ACTOR" "$GHCR_TOKEN" | base64 | tr -d '\n')
  ssh server "mkdir -p /tmp/ghcr && printf '%s' '{\"auths\":{\"ghcr.io\":{\"auth\":\"$AUTH\"}}}' > /tmp/ghcr/config.json"
fi

ssh server "cd $app_dir && DOCKER_CONFIG=/tmp/ghcr IMAGE_TAG=$tag docker-compose pull && echo IMAGE_TAG=$tag > .env && {docker rm -f build-status-dashboard 2>/dev/null || true; } && docker-compose up -d && docker image prune -f > /dev/null"

for _ in $(seq 1 20); do
  if ssh server "curl -fsS -m 5 http://localhost:3000/health" > health.json 2> health.err \
    && jq -e --arg c "$tag" --arg e "$env_name" '.commit == $c and .environment == $e' health.json > /dev/null; then
    echo "$env_name is running $tag"
    cat health.json
    echo
    exit 0
  fi
  sleep 3
done

echo "health check failed on $env_name" >&2
cat health.err health.json >&2
ssh server "cd $app_dir && docker-compose ps && docker-compose logs --tail 50"
exit 1
