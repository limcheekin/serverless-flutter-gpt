# 🤖 FlutterGPT 🤖

> An AI chatbot that can answer questions about Flutter.
> It is powered by OpenAI API and LangChain framework, and
> hosted in AWS Lambda and Qdrant Cloud.
> Feel free to chat with the bot via [Telegram](https://t.me/flutter_gpt_bot).

Therefore, for the correct operation of the chatbot, it is necessary to:

- get OpenAI API key > https://platform.openai.com/account/api-keys. You may be granted some free credits.
- create an AWS account > https://portal.aws.amazon.com/billing/signup, free tier plan is good enough. Also, create access key at https://us-east-1.console.aws.amazon.com/iamv2/home#/security_credentials/access-key-wizard for AWS Lambda deployment.
- create Qdrant account on > https://cloud.qdrant.io/ then create a cluster for vector store.

## :file_folder: Table of Contents

- [General Info](#-general-information)
- [Technologies Used](#-technologies-used)
- [Features](#-features)
- [Requirements For Initial Setup](#-requirements-for-initial-setup)
- [Setup](#-setup)
- [Contact](#-contact)

## ℹ️ General Information

- The chatbot's knowledge is based on information from the [Flutter documentation website](https://github.com/flutter/website), which is hosted at https://docs.flutter.dev/ and was last updated in March 2023. The static HTML files are stored in the `site` directory.
- Generate embeddings from the static HTML files using the OpenAI API and save them to Qdrant Cloud.
- Utilize the Serverless Framework to deploy the `handler.py` code to AWS Lambda.
- Access the Lambda URL to ask questions and receive responses.
- The blog post "[ChatGPT Over Your Data](https://blog.langchain.dev/tutorial-chatgpt-over-your-data/)" provides a clear explanation of how the chatbot operates behind the scene.

## 💻 Technologies Used

- langchain
- openai
- qdrant_client

## 🌟 Features

- Using OpenAI API and language model (ChatGPT) with custom knowledge base.
- Potential multi-channels support

## 👀 Requirements For Initial Setup

- Install [Python](https://www.python.org/about/gettingstarted/), should work with any python version 3.9 and above
- NodeJS and Serverless Framework is not needed unless you want to deploy the code and run serverless commands from your own PC. It is optional.
  - Install [NodeJS](https://nodejs.org/en/), should work with any node version above 16.16.0
  - Install [Serverless Framework](https://www.serverless.com/framework/docs/getting-started)

## 📟 Setup

### 1. 💾 Clone/Download the Repository

### 2. 📦 Create Virtual Environment and Install Dependencies:

```bash
$ cd serverless-flutter-gpt
$ python -m venv venv # create virtual environment "venv"
$ source venv/bin/activate # activate it
$ pip install -r requirements.txt
```

### 3. 📔 Setup environment variables

Append the following environment variables to the `venv/bin/activate` file:

```
export QDRANT_URL = "<The URL of the cluster in Qdrant cloud>"
export QDRANT_API_KEY= "<The API key of the Qdrant cloud account>"
export OPENAI_API_KEY = "<The API key of the OpenAI API>"
```

Re-run the following command to activate environment variables:

```bash
$ source venv/bin/activate
```

### Notes:

Remember to configure the environment variables above manually to Lambda once it is deploy successfully as the step is not implemented in continuous deployment.

### 4. 🆕 Ingest Data (Create Embeddings)

```bash
$ python create_embeddings.py
```

### 5. 🚀 Continuous Deployment to AWS Lambda

The code of querying API `handler.py` of the chatbot is continuous deploy and test by GitHub Action using Serverless Framework on every `git push`. Please look into the .github/workflows/dev.yml file to find out more.

Credentials is needed for AWS deployment, add `AWS_KEY` and `AWS_SECRET` to the repository secrets at `https://github.com/<username>/<repo>/settings/secrets/actions`.

## 💬 Contact

Created by [@limcheekin](https://www.linkedin.com/in/limcheekin/) - feel free to contact me!
