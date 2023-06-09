# Unionize
Anonymous communication for people trying to start a union

## Local development Setup
- Install AWS CLI via homebrew using 
  ```bash
  brew install awscli
  ``` 
  we use this to communicate direclty with AWS via shell commands. [Go here](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-quickstart.html) for additional setup information.
- Install SAM CLI via homebrew using \
  ```bash
  brew install aws-sam-cli
  ````
  this is necessary for deployment of cloudformation templates.
- [Docker](https://docs.docker.com/get-docker/) - So you can build your deployment inside of a container and don't need to install/setup specific runtimes on your personal machine.
---
## Deployment
Make sure docker is running on your machine. Then all you have to do to deploy to AWS is run this bash script
```bash
./deploy.sh
```
The first time your run this you may have to download the correct docker image. That should happen in the background, and may take several minutes. On subsequent deployments you typically won't have to download the image again. When prompted with the change set you'll have to confirm by typing `y`.