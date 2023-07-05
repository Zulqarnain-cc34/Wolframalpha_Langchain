TOOLS_LIST = ['serpapi', 'wolfram-alpha', 'pal-math']
TOOLS_DEFAULT_LIST = ['serpapi', 'pal-math', 'wolfram-alpha']

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

llm_state = None
chain_state = None
express_chain_state = None
history_state = None
tools_list_state = TOOLS_DEFAULT_LIST
trace_chain_state = False
speak_text_state = False
talking_head_state = True
monologue_state = False

# Defaults Inputs
num_words_state = NUM_WORDS_DEFAULT
formality_state = FORMALITY_DEFAULT
anticipation_level_state = EMOTION_DEFAULT
joy_level_state = EMOTION_DEFAULT
trust_level_state = EMOTION_DEFAULT
fear_level_state = EMOTION_DEFAULT
surprise_level_state = EMOTION_DEFAULT
sadness_level_state = EMOTION_DEFAULT
disgust_level_state = EMOTION_DEFAULT
anger_level_state = EMOTION_DEFAULT
lang_level_state = LANG_LEVEL_DEFAULT
translate_to_state = TRANSLATE_TO_DEFAULT
literary_style_state = LITERARY_STYLE_DEFAULT
