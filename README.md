# github-branch-protect
A simple web service listens for GitHub's org events to enable branch protection whenever a new repo is created. It also notifies you with an @mention in an issue within the repository

## Usage
- Install the following:
  - Python 3
  - Virtualenv
    - `pip install -r requirements.txt`
  - Flask
  - ngrok
    

- Set `token` as an environment variable with a GitHub's Token in command prompt (`set token=<token_value>`)
- Set the user value in `app.py`
- Start the local Flask web service via `flask run --host=0.0.0.0 --port=5000`
- Start the ngrok's forwarding service via `ngrok.exe http 5000`
- Copy the forwarding address (`https://<alpha_numeric>.ngrok.io` in the output of the ngrok application)

## GitHub's Org webhook & other settings

- Set up a WebHook in the GitHub organization - [Webhook](https://github.com/organizations/vpcta/settings/hooks/)
  - Paste the forwarding address in the Payload URL - [ngrok](https://<alpha_numeric>.ngrok.io)
  - Content type should be application/json
  - Select `Send me everything.` for the events to be triggered
  - Save the Webhook
    
- Once the webhook is set, modify the default branch name to `master` instead of `main` branch under the repository's settings page - [See here](https://docs.github.com/en/github/administering-a-repository/managing-branches-in-your-repository/changing-the-default-branch)

    
## How to test the setup??

- Start the local Flask webservice
- Keep the ngrok tunneling running in another command prompt
- Create a new repository by keeping the branch public & don't forget to select the `Add a README file`
- See that branch protection will be added and an issue will be created for the repo.

## Dependencies
- Python
- Flask
- ngrok
- GitHub's webhook config

## Reference
- [GitHub APIv3](https://developer.github.com/v3/)
- [Web Hooks](https://developer.github.com/webhooks/)
- [Flask Docs](https://flask.palletsprojects.com/en/1.1.x/)
- [ngrok](https://ngrok.com/docs)

