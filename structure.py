import argparse
import requests, os, urllib3, ssl
from dotenv import load_dotenv
from griptape.configs import Defaults
from griptape.structures import Pipeline
from griptape.tasks import AssistantTask
from griptape.drivers.memory.conversation.griptape_cloud import GriptapeCloudConversationMemoryDriver
from griptape.drivers.ruleset.griptape_cloud import GriptapeCloudRulesetDriver
from griptape.drivers.vector.griptape_cloud import GriptapeCloudVectorStoreDriver
from griptape.drivers.assistant.griptape_cloud import GriptapeCloudAssistantDriver
from griptape.drivers.prompt.griptape_cloud import GriptapeCloudPromptDriver
from griptape.engines.rag import RagEngine
from griptape.engines.rag.modules import (
    PromptResponseRagModule,
    VectorStoreRetrievalRagModule,
)
from griptape.engines.rag.stages import ResponseRagStage, RetrievalRagStage
from griptape.rules.ruleset import Ruleset
from griptape.structures import Agent
from griptape.tools import BaseTool, RagTool
from griptape.utils import GriptapeCloudStructure
from pydantic import BaseModel

load_dotenv()

class Output(BaseModel):
    comprehensive_answer: str

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-k",
        "--knowledge-base-id",
        default=None,
        help="Set the Griptape Cloud Knowledge Base ID you wish to use",
    )
    parser.add_argument(
        "-p",
        "--prompt",
        default="Hello there!",
        help="The prompt you wish to use",
    )
    parser.add_argument(
        "-r",
        "--ruleset-alias",
        default=None,
        help="Set the Griptape Cloud Ruleset alias to use",
    )
    parser.add_argument(
        "-s",
        "--stream",
        default=False,
        action="store_true",
        help="Enable streaming mode for the Agent",
    )
    parser.add_argument(
        "-t",
        "--thread_id",
        default=None,
        help="Set the Griptape Cloud Thread ID you wish to use",
    )

    args = parser.parse_args()
    knowledge_base_id = args.knowledge_base_id
    prompt = "Answer the following question:\n\n" + args.prompt + "\n\nYour response should not include additional information nor actions for the user to fulfil. Respond only using plaintext, do not use any markdown formatting in your response."
    thread_id = args.thread_id
    ruleset_alias = args.ruleset_alias
    stream = args.stream

    Defaults.drivers_config.conversation_memory_driver = GriptapeCloudConversationMemoryDriver(
        thread_id=thread_id,
        base_url=os.environ["GT_CLOUD_BASE_URL"],
        api_key=os.environ["GT_CLOUD_API_KEY"],
    )

    pipeline = Pipeline(
        conversation_memory_strategy="per_task",
        tasks=[
            AssistantTask(
                assistant_driver=GriptapeCloudAssistantDriver(
                    base_url=os.environ["GT_CLOUD_BASE_URL"],
                    assistant_id=os.environ["GT_CLOUD_ASSISTANT_ID"],
                    api_key=os.environ["GT_CLOUD_API_KEY"],
                    stream=False,
                    max_attempts=1,
                    thread_id=thread_id,
                    additional_ruleset_ids = [os.environ["RULES"],],
                ),
            ),
        ]
    )

    with GriptapeCloudStructure():
        pipeline.run(prompt)
