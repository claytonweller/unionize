# unionize
Anonymous communication for people trying to start a union

Local development Setup
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