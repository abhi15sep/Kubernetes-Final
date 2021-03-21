# Flask Ask Radio Cooperativa News

#### Listen Cooperativa Radio news as a serverless Flask-Ask function using Zappa

Based on: https://developer.amazon.com/blogs/alexa/post/8e8ad73a-99e9-4c0f-a7b3-60f92287b0bf/new-alexa-tutorial-deploy-flask-ask-skills-to-aws-lambda-with-zappa

Required steps:

```
# clone source code repo
git clone https://gitlab.com/nicosingh/serverless-functions.git

# create virtual environment
cd serverless-functions
virtualenv cooperativa-news
cd cooperativa-news
source bin/activate

# install dependencies
pip install -r requirements.txt

# create an IAM User with Programatic Access and AdministratorAccess policy
aws configure

# deploy our code using the new User
zappa init
zappa deploy dev

# update our code (optional)
zappa update dev

# delete our code (optional)
zappa undeploy dev
```
