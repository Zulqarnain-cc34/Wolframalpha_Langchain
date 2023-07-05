import os
import urllib.parse
import xml.etree.ElementTree as ET

import requests


class ExtendedWolframAlphaAPIWrapper:
    """An extended wrapper for Wolfram Alpha."""
    def __init__(self):
        self.appid = os.environ['WOLFRAM_ALPHA_APPID']
        self.qp = {
            'units': 'metric',
            'format': 'plaintext,image',
            'primary': True,
            'appid': self.appid,
        }

    def run_plots(self, query: str) -> str:
        """Run query through WolframAlpha and parse result."""
        self.qp['format'] = 'image'
        self.qp['podstate'] = None
        self.qp['input'] = query
        uri = 'http://api.wolframalpha.com/v2/query?' + urllib.parse.urlencode(
            self.qp)
        response = requests.get(uri)
        if response.status_code != 200:
            return "Error: " + response.reason

        doc = ET.fromstring(response.text)
        plot_urls = []
        for pod in doc.findall('.//pod'):
            if pod.get('id') == 'Plot':
                for subpod in pod.findall('.//subpod'):
                    plot_urls.append(subpod.find('img').get('src'))

        if not plot_urls:
            return "No plot found."

        plot_list = '\n'.join(
            [f"{i+1}. {url}" for i, url in enumerate(plot_urls)])
        return f"Answer: {plot_list}"

    def run_step(self, query: str) -> str:
        """Run query through WolframAlpha and parse result."""
        self.qp['format'] = 'plaintext'
        self.qp['podstate'] = 'Result__Step-by-step solution'
        self.qp['input'] = query
        uri = 'http://api.wolframalpha.com/v2/query?' + urllib.parse.urlencode(
            self.qp)
        response = requests.get(uri)
        if response.status_code != 200:
            return "Error: " + response.reason

        doc = ET.fromstring(response.text)
        steps = doc.findall('.//pod/subpod/plaintext')
        solutions = ""
        for i, step in enumerate(steps):
            if step.text is None:
                solutions += "\n"
                continue
            solutions += f"Step {i}: " + step.text + '\n'
        if steps is None:
            return "No step-by-step solution found."

        return f"Step-by-Step-Solutions: \n{solutions}"
