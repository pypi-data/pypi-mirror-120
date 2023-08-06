#!/usr/bin/env bash

PARAM=$1; shift
DEPLOY="no"
IMAGE_NAME=${REGISTRY:-"docker.nimworks.com"}"/wilddog"

if [ "$PARAM" = "--push" ]; then
  DEPLOY="yes";
fi

if [ -z ${BRANCH_NAME+x} ]; then
  GIT_BRANCH=$(git symbolic-ref --short -q HEAD);
else
  GIT_BRANCH=${BRANCH_NAME};
fi

# replace slashes with underscore
GIT_BRANCH=${GIT_BRANCH/\//_}

# keep track of tags for pushing
TAGS=("$IMAGE_NAME:$GIT_BRANCH")

# initial build command
BUILD_COMMAND=(build -t "$IMAGE_NAME:$GIT_BRANCH")

# add latest tag if branch is master
if [ "$GIT_BRANCH" = "master" ]; then
  TAGS+=("$IMAGE_NAME:latest")
  BUILD_COMMAND+=(-t "${TAGS[1]}")
fi

docker "${BUILD_COMMAND[@]}" .

if [ "$DEPLOY" = "yes" ]; then
  for tag in "${TAGS[@]}"; do
    docker push "$tag";
  done
fi
