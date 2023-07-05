import os
import re
import sys
# Console to variable
from io import StringIO
from threading import Lock
from typing import Optional, Tuple

from langchain import ConversationChain, LLMChain
from langchain.agents import Tool, initialize_agent, load_tools
from langchain.chains.conversation.memory import ConversationBufferMemory
from langchain.llms import OpenAI
# Pertains to Express-inator functionality
from langchain.prompts import PromptTemplate
from openai.error import (AuthenticationError, InvalidRequestError,
                          RateLimitError)

from wolfram_custom_tool import ExtendedWolframAlphaAPIWrapper

TOOLS_LIST = ['serpapi', 'wolfram-alpha']
TOOLS_DEFAULT_LIST = ['serpapi', 'wolfram-alpha']

BUG_FOUND_MSG = "Congratulations, you've found a bug in this application!"
AUTH_ERR_MSG = "Please paste your OpenAI key from openai.com to use this application. It is not necessary to hit a button or key after pasting it."
MAX_TOKENS = 512

# Pertains to Express-inator functionality
NUM_WORDS_DEFAULT = 0
MAX_WORDS = 400
FORMALITY_DEFAULT = "N/A"
TEMPERATURE_DEFAULT = 0.5
EMOTION_DEFAULT = "N/A"
LANG_LEVEL_DEFAULT = "N/A"
TRANSLATE_TO_DEFAULT = "N/A"
LITERARY_STYLE_DEFAULT = "N/A"

PROMPT_TEMPLATE = PromptTemplate(
    input_variables=[
        "original_words", "num_words", "formality", "emotions", "lang_level",
        "translate_to", "literary_style"
    ],
    template="""Restate {num_words}{formality}{emotions}{lang_level}
    {translate_to}{literary_style}the following: \n{original_words}\n""",
)

os.environ[
    "SERPAPI_API_KEY"] = '543ba6444cbd6fa447a71e9d6cf9d36049c945fa8b3a6a590010abce5c749a1b'
os.environ['WOLFRAM_ALPHA_APPID'] = '44ERXQ-P43EQQTLPA'

# os.environ['GOOGLE_API_KEY'] = ''


# Pertains to Express-inator functionality
def transform_text(desc, express_chain, num_words, formality,
                   anticipation_level, joy_level, trust_level, fear_level,
                   surprise_level, sadness_level, disgust_level, anger_level,
                   lang_level, translate_to, literary_style):
    num_words_prompt = ""
    if num_words and int(num_words) != 0:
        num_words_prompt = "using up to " + str(num_words) + " words, "

    # Change some arguments to lower case
    formality = formality.lower()
    anticipation_level = anticipation_level.lower()
    joy_level = joy_level.lower()
    trust_level = trust_level.lower()
    fear_level = fear_level.lower()
    surprise_level = surprise_level.lower()
    sadness_level = sadness_level.lower()
    disgust_level = disgust_level.lower()
    anger_level = anger_level.lower()

    formality_str = ""
    if formality != "n/a":
        formality_str = "in a " + formality + " manner, "

    # put all emotions into a list
    emotions = []
    if anticipation_level != "n/a":
        emotions.append(anticipation_level)
    if joy_level != "n/a":
        emotions.append(joy_level)
    if trust_level != "n/a":
        emotions.append(trust_level)
    if fear_level != "n/a":
        emotions.append(fear_level)
    if surprise_level != "n/a":
        emotions.append(surprise_level)
    if sadness_level != "n/a":
        emotions.append(sadness_level)
    if disgust_level != "n/a":
        emotions.append(disgust_level)
    if anger_level != "n/a":
        emotions.append(anger_level)

    emotions_str = ""
    if len(emotions) > 0:
        if len(emotions) == 1:
            emotions_str = "with emotion of " + emotions[0] + ", "
        else:
            emotions_str = "with emotions of " + \
                ", ".join(emotions[:-1]) + " and " + emotions[-1] + ", "

    lang_level_str = ""
    if lang_level != LANG_LEVEL_DEFAULT:
        lang_level_str = "at a " + lang_level + \
            " level, " if translate_to == TRANSLATE_TO_DEFAULT else ""

    translate_to_str = ""
    if translate_to != TRANSLATE_TO_DEFAULT:
        translate_to_str = "translated to " + \
            ("" if lang_level == TRANSLATE_TO_DEFAULT else lang_level + " level ") + translate_to + ", "

    literary_style_str = ""
    if literary_style != LITERARY_STYLE_DEFAULT:
        if literary_style == "Prose":
            literary_style_str = "as prose, "
        elif literary_style == "Summary":
            literary_style_str = "as a summary, "
        elif literary_style == "Outline":
            literary_style_str = "as an outline numbers and lower case letters, "
        elif literary_style == "Bullets":
            literary_style_str = "as bullet points using bullets, "
        elif literary_style == "Poetry":
            literary_style_str = "as a poem, "
        elif literary_style == "Haiku":
            literary_style_str = "as a haiku, "
        elif literary_style == "Limerick":
            literary_style_str = "as a limerick, "
        elif literary_style == "Joke":
            literary_style_str = "as a very funny joke with a setup and punchline, "
        elif literary_style == "Knock-knock":
            literary_style_str = "as a very funny knock-knock joke, "

    formatted_prompt = PROMPT_TEMPLATE.format(
        original_words=desc,
        num_words=num_words_prompt,
        formality=formality_str,
        emotions=emotions_str,
        lang_level=lang_level_str,
        translate_to=translate_to_str,
        literary_style=literary_style_str)

    trans_instr = num_words_prompt + formality_str + emotions_str + \
        lang_level_str + translate_to_str + literary_style_str
    if express_chain and len(trans_instr.strip()) > 0:
        generated_text = express_chain.run({
            'original_words': desc,
            'num_words': num_words_prompt,
            'formality': formality_str,
            'emotions': emotions_str,
            'lang_level': lang_level_str,
            'translate_to': translate_to_str,
            'literary_style': literary_style_str
        }).strip()
    else:
        generated_text = desc

    # replace all newlines with <br> in generated_text
    generated_text = generated_text.replace("\n", "\n\n")

    return generated_text


def load_chain(tools_list, llm):
    chain = None
    express_chain = None
    if llm:
        tool_names = tools_list
        tools = load_tools(
            tool_names,
            llm=llm,
        )
        wolfram_tools = [
            Tool(
                name="Wolfram Alpha Step by Step Solution",
                func=ExtendedWolframAlphaAPIWrapper().run_step,
                description="A wrapper around Wolfram Alpha. Useful for getting the step by step solution s to questions about Math, Science, Technology, Culture, Society and Everyday Life. Input should be a search query.",
            ),
            Tool(
                name="Wolfram Alpha Images List",
                func=ExtendedWolframAlphaAPIWrapper().run_plots,
                description="Useful for returning the links to plot genereted by query about Math, Science, Technology, Culture, Society and Everyday Life. Input should be a query Output is a string with the urls of generated plots",
            )
        ]
        all_tools = tools + wolfram_tools
        memory = ConversationBufferMemory(memory_key="chat_history")
        # Two chains one is optimized for conversation and
        # other for options we can call the express chain
        # to express the convo in different formats like tone,language etc
        chain = initialize_agent(all_tools,
                                 llm,
                                 agent="zero-shot-react-description",
                                 verbose=True,
                                 memory=memory)
        express_chain = LLMChain(llm=llm, prompt=PROMPT_TEMPLATE, verbose=True)
    return chain, express_chain


def set_openai_api_key(api_key):
    """Set the api key and return chain.
    If no api_key, then None is returned.
    """
    if api_key and api_key.startswith("sk-") and len(api_key) > 50:
        os.environ["OPENAI_API_KEY"] = api_key
        llm = OpenAI(temperature=0, max_tokens=MAX_TOKENS)
        chain, express_chain = load_chain(TOOLS_DEFAULT_LIST, llm)
        return chain, express_chain, llm
    return None, None, None


def run_chain(chain, inp, capture_hidden_text):
    output = ""
    hidden_text = None
    if capture_hidden_text:
        error_msg = None
        tmp = sys.stdout
        hidden_text_io = StringIO()
        sys.stdout = hidden_text_io

        try:
            output = chain.run(input=inp)
        except AuthenticationError as ae:
            error_msg = AUTH_ERR_MSG
        except RateLimitError as rle:
            error_msg = "\n\nRateLimitError: " + str(rle)
        except ValueError as ve:
            error_msg = "\n\nValueError: " + str(ve)
        except InvalidRequestError as ire:
            error_msg = "\n\nInvalidRequestError: " + str(ire)
        except Exception as e:
            error_msg = "\n\n" + BUG_FOUND_MSG + ":\n\n" + str(e)

        sys.stdout = tmp
        hidden_text = hidden_text_io.getvalue()

        # remove escape characters from hidden_text
        hidden_text = re.sub(r'\x1b[^m]*m', '', hidden_text)

        # remove "Entering new AgentExecutor chain..." from hidden_text
        hidden_text = re.sub(r"Entering new AgentExecutor chain...\n", "",
                             hidden_text)

        # remove "Finished chain." from hidden_text
        hidden_text = re.sub(r"Finished chain.", "", hidden_text)

        # Add newline after "Thought:" "Action:" "Observation:" "Input:" and "AI:"
        hidden_text = re.sub(r"Thought:", "\n\nThought:", hidden_text)
        hidden_text = re.sub(r"Action:", "\n\nAction:", hidden_text)
        hidden_text = re.sub(r"Observation:", "\n\nObservation:", hidden_text)
        hidden_text = re.sub(r"Input:", "\n\nInput:", hidden_text)
        hidden_text = re.sub(r"AI:", "\n\nAI:", hidden_text)

        if error_msg:
            hidden_text += error_msg

    else:
        try:
            output = chain.run(input=inp)
        except AuthenticationError as ae:
            output = AUTH_ERR_MSG
        except RateLimitError as rle:
            output = "\n\nRateLimitError: " + str(rle)
        except ValueError as ve:

            output = "\n\nValueError: " + str(ve)
        except InvalidRequestError as ire:
            output = "\n\nInvalidRequestError: " + str(ire)
        except Exception as e:
            output = "\n\n" + BUG_FOUND_MSG + ":\n\n" + str(e)

    return output, hidden_text


class ChatWrapper:
    def __init__(self):
        self.lock = Lock()

    def __call__(self, api_key: str, inp: str, history: Optional[Tuple[str,
                                                                       str]],
                 chain: Optional[ConversationChain], trace_chain: bool,
                 monologue: bool, express_chain: Optional[LLMChain], num_words,
                 formality, anticipation_level, joy_level, trust_level,
                 fear_level, surprise_level, sadness_level, disgust_level,
                 anger_level, lang_level, translate_to, literary_style):
        """Execute the chat functionality."""
        self.lock.acquire()
        try:
            # If history is given then good otherwise empty
            history = history or []

            # If chain is None, that is because no API key was provided.
            output = "Please paste your OpenAI key from openai.com to use this application. It is not necessary to hit a button or " \
                     "key after pasting it."

            if chain:
                # Set OpenAI key
                import openai
                openai.api_key = api_key
                if not monologue:
                    output, hidden_text = run_chain(
                        chain, inp, capture_hidden_text=trace_chain)
                    print(output)
                else:
                    output = inp

            output = transform_text(output, express_chain, num_words,
                                    formality, anticipation_level, joy_level,
                                    trust_level, fear_level, surprise_level,
                                    sadness_level, disgust_level, anger_level,
                                    lang_level, translate_to, literary_style)

            text_to_display = output
            if trace_chain:
                text_to_display = output
            history.append((inp, text_to_display))

        except Exception as e:
            raise e
        finally:
            self.lock.release()
        return history
