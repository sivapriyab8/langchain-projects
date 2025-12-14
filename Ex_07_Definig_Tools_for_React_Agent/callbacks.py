from langchain_core.callbacks import BaseCallbackHandler

class AgentCallbackHandler(BaseCallbackHandler):
    def on_llm_start(self, serialized, prompts, **kwargs):
        print("\n--- LLM START ---")
        print(prompts)

    def on_llm_end(self, response, **kwargs):
        print("\n--- LLM END ---")
        print(response)

    def on_tool_start(self, serialized, input_str, **kwargs):
        print("\n--- TOOL START ---")
        print(f"Tool: {serialized.get('name')}")
        print(f"Input: {input_str}")

    def on_tool_end(self, output, **kwargs):
        print("\n--- TOOL END ---")
        print(output)

    def on_agent_action(self, action, **kwargs):
        print("\n--- AGENT ACTION ---")
        print(action)
