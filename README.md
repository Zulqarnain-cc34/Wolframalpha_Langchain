Api Documentation:

Endpoint: /prompt

Method: POST

Input:

    prompt: A string representing the prompt text to be used to generate text. Default is "How's the weather?"
    API-KEY: A header field containing the API Key provided by OpenAI to access the language model.

Output:

    A string of generated text based on the prompt and API Key.
    401 status code with message "API Key is missing" if the API-KEY header field is not provided.
    500 status code with message "Server Internal error" if there is an error processing the request.

Description:
This endpoint is used to generate text using OpenAI's language model. The endpoint takes a prompt and API Key as input and returns the generated text as output. The endpoint requires an API Key to be provided in the API-KEY header field to access the language model. If the API Key is not provided, the endpoint returns a 401 status code with a message of "API Key is missing". If there is an error processing the request, the endpoint returns a 500 status code with a message of "Server Internal error".
