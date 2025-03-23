import argparse
import os
from dotenv import load_dotenv
from griptape.configs import Defaults
from griptape.structures import Pipeline
from griptape.tasks import AssistantTask
from griptape.drivers.memory.conversation.griptape_cloud import GriptapeCloudConversationMemoryDriver
from griptape.drivers.ruleset.griptape_cloud import GriptapeCloudRulesetDriver
from griptape.drivers.vector.griptape_cloud import GriptapeCloudVectorStoreDriver
from griptape.drivers.assistant.griptape_cloud import GriptapeCloudAssistantDriver
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

load_dotenv()

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
    prompt = args.prompt
    thread_id = args.thread_id
    ruleset_alias = args.ruleset_alias
    stream = args.stream

    Defaults.drivers_config.conversation_memory_driver = GriptapeCloudConversationMemoryDriver(
        thread_id=thread_id,
    )

    pipeline = Pipeline(
        conversation_memory_strategy="per_task",
        tasks=[
            AssistantTask(
                assistant_driver=GriptapeCloudAssistantDriver(
                    assistant_id=os.environ["GT_CLOUD_ASSISTANT_ID"],
                    api_key=os.environ["GT_CLOUD_API_KEY"],
                    stream=False,
                ),
            ),
        ]
    )

    with GriptapeCloudStructure():
        pipeline.run(prompt)
