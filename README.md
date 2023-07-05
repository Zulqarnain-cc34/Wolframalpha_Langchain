<div align="center"><p>
    <a href="https://github.com/Zulqarnain-cc34/Wolframalpha_Langchain/releases/latest">
      <img alt="Latest release" src="https://img.shields.io/github/v/release/Zulqarnain-cc34/Wolframalpha_Langchain?style=for-the-badge&logo=starship&color=C9CBFF&logoColor=D9E0EE&labelColor=302D41&include_prerelease&sort=semver" />
    </a>
    <a href="https://github.com/Zulqarnain-cc34/Wolframalpha_Langchain/pulse">
      <img alt="Last commit" src="https://img.shields.io/github/last-commit/Zulqarnain-cc34/Wolframalpha_Langchain?style=for-the-badge&logo=starship&color=8bd5ca&logoColor=D9E0EE&labelColor=302D41"/>
    </a>
    <a href="https://github.com/Zulqarnain-cc34/Wolframalpha_Langchain/blob/main/LICENSE">
      <img alt="License" src="https://img.shields.io/github/license/Zulqarnain-cc34/Wolframalpha_Langchain?style=for-the-badge&logo=starship&color=ee999f&logoColor=D9E0EE&labelColor=302D41" />
    </a>
    <a href="https://github.com/Zulqarnain-cc34/Wolframalpha_Langchain/stargazers">
      <img alt="Stars" src="https://img.shields.io/github/stars/Zulqarnain-cc34/Wolframalpha_Langchain?style=for-the-badge&logo=starship&color=c69ff5&logoColor=D9E0EE&labelColor=302D41" />
    </a>
    <a href="https://github.com/Zulqarnain-cc34/Wolframalpha_Langchain">
      <img alt="Repo Size" src="https://img.shields.io/github/repo-size/Zulqarnain-cc34/Wolframalpha_Langchain?color=%23DDB6F2&label=SIZE&logo=codesandbox&style=for-the-badge&logoColor=D9E0EE&labelColor=302D41" />
    </a>
</div>


# Wolfram Alpha Wrapper

Wolfram Alpha tool wrapper is a Python tool that provides an extended wrapper for Wolfram Alpha API. It allows you to retrieve plot images and step-by-step solutions for a given query.

### Features

- **Plot Retrieval**: Obtains url of plot images for a given query.
- **Step-by-Step Solutions**: Get step-by-step solutions for a query.

### Getting Started

1. Obtain a Wolfram Alpha App ID.
2. Set the `WOLFRAM_ALPHA_APPID` environment variable with your App ID.
3. Set the `SERPAPI_API_KEY` environment variable with your App ID.

To change it in `chat.py`.

<div>
  <img src="./assets/wolfram.png">
</div>

In case you want to use Docker. To run use `docker build .`

### Query

To change the `test.py` file and run using python.

```python

url = "http://172.17.0.2:5000/prompt"

headers = {
    'Content-Type': 'application/json',
    'API-KEY': 'API-KEY'
}

data = {'prompt': 'Paste prompt here'}

response = requests.post(url, headers=headers, json=data)

print(response.text)

```
