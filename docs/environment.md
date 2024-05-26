# Environment 

```dotenv
# API Keys
LANGCHAIN_API_KEY=[REQUIRED]
SERPAPI_API_KEY=[REQUIRED]
APP_DIALOGUE_MODEL_API_KEY="[REQUIRED for some models]"

# Chat Model
APP_DIALOGUE_MODEL_PROVIDER=openai
APP_DIALOGUE_MODEL=gpt-4
APP_DIALOGUE_MODEL_TEMPERATURE=0.2

# Dialogue
#######################################
# The personas should match the topic #
#######################################
# Comma seperated list of personas e.g: "AI enthusiast, AI skeptic" or "Atheist, Christian"
APP_DIALOGUE_PERSONAS=[REQUIRED]
APP_DIALOGUE_TOPIC=[REQUIRED]
APP_DIALOGUE_MODERATOR=Moderator
# Optional
APP_DIALOGUE_MAX_TURNS=6

# Docker
DOCKER_IMAGE_TAG=latest
```