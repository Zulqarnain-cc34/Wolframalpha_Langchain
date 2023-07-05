from flask import Flask, request

import config
from chat import ChatWrapper, set_openai_api_key

app = Flask(__name__)
app.secret_key = "secret-key"

# Making the Chat Wrapper
chat = ChatWrapper()


@app.route("/prompt", methods=["POST"])
def prompt_route():
    # Get the prompt from the request data
    data = request.get_json()
    if data is not None:
        prompt = data.get("prompt")
    else:
        prompt = "How's the weather?"

    api_key = request.headers.get("API-KEY")

    if api_key is None:
        return "API Key is missing", 401

    chain_state, express_chain_state, llm_state = set_openai_api_key(
        api_key=api_key)

    # Calling the Langchain API with default and input
    history = chat.__call__(api_key=api_key,
                            inp=prompt,
                            history=None,
                            chain=chain_state,
                            express_chain=express_chain_state,
                            formality=config.formality_state,
                            trace_chain=config.trace_chain_state,
                            monologue=config.monologue_state,
                            num_words=config.num_words_state,
                            anticipation_level=config.anticipation_level_state,
                            joy_level=config.joy_level_state,
                            trust_level=config.trust_level_state,
                            fear_level=config.fear_level_state,
                            surprise_level=config.surprise_level_state,
                            sadness_level=config.sadness_level_state,
                            disgust_level=config.disgust_level_state,
                            anger_level=config.anger_level_state,
                            lang_level=config.lang_level_state,
                            translate_to=config.translate_to_state,
                            literary_style=config.literary_style_state)

    if history is not None:
        return history[0][1]
    return 'Server Internal error', 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
