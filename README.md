# aidebate

## Easily automate a debate between 2 or more AI agents

Simply set the debate topic and list of personas, 
run the app and watch the AI personas debate.
 
### Quick Start

1. Install the app by running [shell/install.sh](shell/install.sh) in a command prompt.

2. Set required environment variables:

    ```dotenv
    LANGCHAIN_API_KEY=[REQUIRED]
    SERPAPI_API_KEY=[REQUIRED]
    APP_DIALOGUE_MODEL_API_KEY=[REQUIRED]

    # Comma seperated list of personas e.g: "AI enthusiast, AI skeptic" or "Atheist, Christian"
    APP_DIALOGUE_PERSONAS="Atheist, Christian"
    APP_DIALOGUE_TOPIC="Was the universe created by an intelligent designer?"

    APP_DIALOGUE_MODEL_PROVIDER="[OPTIONAL, default=openai]"
    APP_DIALOGUE_MODEL="[OPTIONAL, default=gpt-4]"
    ```
    
    For a full ist of environment variables, see [Environment](docs/environment.md).

3. Run the app by running [shell/run.sh](shell/run.sh) in a command prompt. 

### Notes

* Based on the fabulous work being done by [langchain](https://www.langchain.com/).
* [List of supported LLMs](docs/supported-models.md).
* The topic should match the personas for example:

    ```
    Topic: "The impact of automation and artificial intelligence on employment."
    Personas: "AI enthusiast, AI skeptic"
    ```

    ```
    Topic: "Was the universe created by an intelligent designer?"
    Personas: "Atheist, Christian"
    ```
  
### Changing LLM

For example to use `anthropic` instead of `openai`:

* Only openai is installed by default. So install anthropic: `pip install -qU langchain-anthropic`.

* In your environment set the provider/model (`anthropic`) related properties. 

    ```dotenv
    APP_DIALOGUE_MODEL_API_KEY=[REQUIRED]
    APP_DIALOGUE_MODEL_PROVIDER=anthropic
    APP_DIALOGUE_MODEL="claude-3-opus-20240229" # or any other model
    ```
  
* Go through the steps in the quick start section above.

