from dotenv import load_dotenv
import llm.anthropic.client
import llm.gemini.client
import llm.grok.client
import llm.openai.client
from llm.base import Message
from utils.data_handler import DataHandler
from utils.date import get_current_time_str
import os

load_dotenv()


data_handler = DataHandler()
llm_clients = [
    llm.anthropic.client.AnthropicLLM(),
    llm.gemini.client.GeminiLLM(),
    llm.grok.client.GrokLLM(),
    llm.openai.client.OpenAILLM(),
]
PROMPTS_FOLDER = "prompts"
PROMPTS_FILE = "lang_explanation.json"
RESULTS_FOLDER = "results"

if __name__ == "__main__":
    prompts = data_handler.load(
        os.path.join(PROMPTS_FOLDER, PROMPTS_FILE), format="json"
    )
    clients = llm_clients[:1]

    for client in clients:
        for prompt in prompts["contents"]:
            response = client.single_response([Message(role="user", content=prompt)])
            print(response.content)
            data_handler.save(
                response.content,
                os.path.join(
                    RESULTS_FOLDER,
                    f"{PROMPTS_FILE.split('.')[0]}_{client.name}_{get_current_time_str()}.json",
                ),
                format="json",
            )
