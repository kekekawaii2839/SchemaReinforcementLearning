from bfcl.model_handler.oss_model.deepseek import DeepseekHandler
from bfcl.model_handler.oss_model.gemma import GemmaHandler
from bfcl.model_handler.oss_model.glaive import GlaiveHandler
from bfcl.model_handler.oss_model.glm import GLMHandler
from bfcl.model_handler.oss_model.granite import GraniteHandler
from bfcl.model_handler.oss_model.hammer import HammerHandler
from bfcl.model_handler.oss_model.hermes import HermesHandler
from bfcl.model_handler.oss_model.llama import LlamaHandler
from bfcl.model_handler.oss_model.llama_fc import LlamaFCHandler
from bfcl.model_handler.oss_model.phi import PhiHandler
from bfcl.model_handler.oss_model.salesforce import SalesforceHandler
from bfcl.model_handler.oss_model.qwen import QwenHandler
from bfcl.model_handler.oss_model.minicpm import MiniCPMHandler
from bfcl.model_handler.proprietary_model.claude import ClaudeHandler
from bfcl.model_handler.proprietary_model.cohere import CohereHandler
from bfcl.model_handler.proprietary_model.databricks import DatabricksHandler
from bfcl.model_handler.proprietary_model.fireworks import FireworksHandler
from bfcl.model_handler.proprietary_model.functionary import FunctionaryHandler
from bfcl.model_handler.proprietary_model.gemini import GeminiHandler
from bfcl.model_handler.proprietary_model.gorilla import GorillaHandler
from bfcl.model_handler.proprietary_model.mistral import MistralHandler
from bfcl.model_handler.proprietary_model.nexus import NexusHandler
from bfcl.model_handler.proprietary_model.nvidia import NvidiaHandler
from bfcl.model_handler.proprietary_model.openai import OpenAIHandler
from bfcl.model_handler.proprietary_model.yi import YiHandler
from bfcl.model_handler.proprietary_model.gogoagent import GoGoAgentHandler

# TODO: Add Deepseek V2, meta-llama/Llama-3.1-405B-Instruct

# Inference through API calls
api_inference_handler_map = {
    "gorilla-openfunctions-v2": GorillaHandler,
    "o1-preview-2024-09-12": OpenAIHandler,
    "o1-mini-2024-09-12": OpenAIHandler,
    "gpt-4o-2024-08-06": OpenAIHandler,
    "gpt-4o-2024-08-06-FC": OpenAIHandler,
    "gpt-4o-mini-2024-07-18": OpenAIHandler,
    "gpt-4o-mini-2024-07-18-FC": OpenAIHandler,
    "gpt-4-turbo-2024-04-09": OpenAIHandler,
    "gpt-4-turbo-2024-04-09-FC": OpenAIHandler,
    "gpt-3.5-turbo-0125": OpenAIHandler,
    "gpt-3.5-turbo-0125-FC": OpenAIHandler,
    "claude-3-opus-20240229": ClaudeHandler,
    "claude-3-opus-20240229-FC": ClaudeHandler,
    "claude-3-sonnet-20240229": ClaudeHandler,
    "claude-3-sonnet-20240229-FC": ClaudeHandler,
    "claude-3-haiku-20240307": ClaudeHandler,
    "claude-3-haiku-20240307-FC": ClaudeHandler,
    "claude-3-5-sonnet-20240620": ClaudeHandler,
    "claude-3-5-sonnet-20240620-FC": ClaudeHandler,
    "open-mistral-nemo-2407": MistralHandler,
    "open-mistral-nemo-2407-FC": MistralHandler,
    "open-mixtral-8x22b": MistralHandler,
    "open-mixtral-8x22b-FC": MistralHandler,
    "open-mixtral-8x7b": MistralHandler,
    "mistral-large-2407": MistralHandler,
    "mistral-large-2407-FC": MistralHandler,
    "mistral-medium-2312": MistralHandler,
    "mistral-small-2402": MistralHandler,
    "mistral-small-2402-FC": MistralHandler,
    "firefunction-v1-FC": FireworksHandler,
    "firefunction-v2-FC": FireworksHandler,
    "Nexusflow-Raven-v2": NexusHandler,
    "gemini-1.5-pro-002": GeminiHandler,
    "gemini-1.5-pro-002-FC": GeminiHandler,
    "gemini-1.5-pro-001": GeminiHandler,
    "gemini-1.5-pro-001-FC": GeminiHandler,
    "gemini-1.5-flash-002": GeminiHandler,
    "gemini-1.5-flash-002-FC": GeminiHandler,
    "gemini-1.5-flash-001": GeminiHandler,
    "gemini-1.5-flash-001-FC": GeminiHandler,
    "gemini-1.0-pro-002": GeminiHandler,
    "gemini-1.0-pro-002-FC": GeminiHandler,
    "meetkai/functionary-small-v3.1-FC": FunctionaryHandler,
    "meetkai/functionary-medium-v3.1-FC": FunctionaryHandler,
    "databricks-dbrx-instruct": DatabricksHandler,
    "command-r-plus-FC": CohereHandler,
    "command-r-plus": CohereHandler,
    "command-r-plus-FC-optimized": CohereHandler,
    "command-r-plus-optimized": CohereHandler,
    "snowflake/arctic": NvidiaHandler,
    "nvidia/nemotron-4-340b-instruct": NvidiaHandler,
    "BitAgent/GoGoAgent": GoGoAgentHandler,
    # "yi-large-fc": YiHandler,  #  Their API is under maintenance, and will not be back online in the near future
}

# Inference through local hosting
local_inference_handler_map = {
    "google/gemma-2-2b-it": GemmaHandler,
    "google/gemma-2-9b-it": GemmaHandler,
    "google/gemma-2-27b-it": GemmaHandler,
    "meta-llama/Meta-Llama-3-8B-Instruct": LlamaHandler,
    "meta-llama/Meta-Llama-3-70B-Instruct": LlamaHandler,
    "meta-llama/Llama-3.1-8B-Instruct-FC": LlamaFCHandler,
    "meta-llama/Llama-3.1-70B-Instruct-FC": LlamaFCHandler,
    "meta-llama/Llama-3.2-1B-Instruct-FC": LlamaFCHandler,
    "meta-llama/Llama-3.2-3B-Instruct-FC": LlamaFCHandler,
    "meta-llama/Llama-3.1-8B-Instruct": LlamaHandler,
    "meta-llama/Llama-3.1-70B-Instruct": LlamaHandler,
    "meta-llama/Llama-3.2-1B-Instruct": LlamaHandler,
    "meta-llama/Llama-3.2-3B-Instruct": LlamaHandler,
    "Salesforce/xLAM-1b-fc-r": SalesforceHandler,
    "Salesforce/xLAM-7b-fc-r": SalesforceHandler,
    "Salesforce/xLAM-7b-r": SalesforceHandler,
    "Salesforce/xLAM-8x22b-r": SalesforceHandler,
    "Salesforce/xLAM-8x7b-r": SalesforceHandler,
    "microsoft/Phi-3-mini-4k-instruct": PhiHandler,
    "microsoft/Phi-3-mini-128k-instruct": PhiHandler,
    "microsoft/Phi-3-small-8k-instruct": PhiHandler,
    "microsoft/Phi-3-small-128k-instruct": PhiHandler,
    "microsoft/Phi-3-medium-4k-instruct": PhiHandler,
    "microsoft/Phi-3-medium-128k-instruct": PhiHandler,
    "microsoft/Phi-3.5-mini-instruct": PhiHandler,
    "NousResearch/Hermes-2-Pro-Mistral-7B": HermesHandler,
    "NousResearch/Hermes-2-Pro-Llama-3-8B": HermesHandler,
    "NousResearch/Hermes-2-Theta-Llama-3-8B": HermesHandler,
    "NousResearch/Hermes-2-Pro-Llama-3-70B": HermesHandler,
    "NousResearch/Hermes-2-Theta-Llama-3-70B": HermesHandler,
    "ibm-granite/granite-20b-functioncalling": GraniteHandler,
    "MadeAgents/Hammer2.0-7b": HammerHandler,
    "MadeAgents/Hammer2.0-3b": HammerHandler,
    "MadeAgents/Hammer2.0-1.5b": HammerHandler,
    "MadeAgents/Hammer2.0-0.5b": HammerHandler,
    "THUDM/glm-4-9b-chat": GLMHandler,
    "Qwen/Qwen2-1.5B-Instruct": QwenHandler,
    "Qwen/Qwen2-7B-Instruct": QwenHandler,
    "Qwen/Qwen2.5-1.5B-Instruct": QwenHandler,
    "Qwen/Qwen2.5-7B-Instruct": QwenHandler,
    "Team-ACE/ToolACE-8B": LlamaHandler,
    "openbmb/MiniCPM3-4B": MiniCPMHandler,
    "/home/test/test03/objlink/Meta-Llama-3.1-8B-Instruct": LlamaHandler,
}

# schemabench
handler_list = [
    DeepseekHandler,
    GemmaHandler,
    GlaiveHandler,
    GLMHandler,
    GraniteHandler,
    HammerHandler,
    HermesHandler,
    LlamaHandler,
    LlamaFCHandler,
    PhiHandler,
    PhiHandler,
    SalesforceHandler,
    QwenHandler,
    MiniCPMHandler,
    ClaudeHandler,
    CohereHandler,
    DatabricksHandler,
    FireworksHandler,
    FunctionaryHandler,
    GeminiHandler,
    GorillaHandler,
    MistralHandler,
    NexusHandler,
    NvidiaHandler,
    OpenAIHandler,
    YiHandler,
    GoGoAgentHandler,
]

import json
with open('./schemabench/berkeley-function-call-leaderboard/local_model_config.json', 'r', encoding='utf-8') as f:
    local_handler = json.load(f)
for h in local_handler:
    model_path = h['model_path']
    model_handler = None
    for handler in handler_list:
        if handler.__name__ == h['model_handler']:
            model_handler = handler
            break
    if model_handler is None:
        raise Exception("Unknown handler, please check your config")
    local_inference_handler_map[model_path] = model_handler
    model_path = model_path.replace('_', '/')
    local_inference_handler_map[model_path] = model_handler

# Deprecated/outdated models, no longer on the leaderboard
outdated_model_handler_map = {
    # "gorilla-openfunctions-v0": GorillaHandler,
    # "gpt-4o-2024-05-13": OpenAIHandler,
    # "gpt-4o-2024-05-13-FC": OpenAIHandler,
    # "gpt-4-1106-preview-FC": OpenAIHandler,
    # "gpt-4-1106-preview": OpenAIHandler,
    # "gpt-4-0125-preview-FC": OpenAIHandler,
    # "gpt-4-0125-preview": OpenAIHandler,
    # "gpt-4-0613-FC": OpenAIHandler,
    # "gpt-4-0613": OpenAIHandler,
    # "claude-2.1": ClaudeHandler,
    # "claude-instant-1.2": ClaudeHandler,
    # "gemini-1.0-pro-001": GeminiHandler,
    # "gemini-1.0-pro-001-FC": GeminiHandler,
    # "meetkai/functionary-small-v3.1-FC": FunctionaryHandler,
    # "mistral-tiny-2312": MistralHandler,
    # "glaiveai/glaive-function-calling-v1": GlaiveHandler,
    # "google/gemma-7b-it": GemmaHandler,
    # "deepseek-ai/deepseek-coder-6.7b-instruct": DeepseekHandler,
}

HANDLER_MAP = {**api_inference_handler_map, **local_inference_handler_map}
