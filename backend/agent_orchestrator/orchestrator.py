"""
Orchestrator — this IS the agentic part.

Gemini gets the user's question + tool definitions. It decides which
tool to call, calls it, sees the result, decides the NEXT tool to call
(or gives a final answer). This loop runs until Gemini stops asking
for tools — that's the multi-step, deterministic agent behavior.

Needs GOOGLE_API_KEY env var + pip install google-genai
"""
import os
from google import genai
from google.genai import types

from tools import TOOL_REGISTRY

_SYSTEM_INSTRUCTION = """You are SyncRights' compliance agent. You help
answer music-rights usage questions by calling tools in sequence:

1. Use search_catalog to find the track/version the user is asking about.
2. Use check_usage_rights to check if that exact version is cleared for
   the requested usage type (advertisement, ott, movie, trailer, etc).
3. If usage_allowed is false, use get_alternative_recommendations to
   suggest a cleared alternative.
4. Give a final plain-English verdict: cleared, not cleared, or
   suggest an alternative — cite the specific rights holders and
   reasoning from the tool results. Do not invent tracks or rights
   that didn't come from a tool call.
"""

_TOOL_DECLARATIONS = [
    {
        "name": "search_catalog",
        "description": "Search the music catalog by track title or artist name.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Track title or artist name"},
            },
            "required": ["query"],
        },
    },
    {
        "name": "check_usage_rights",
        "description": "Check whether a specific track version is cleared for a usage type.",
        "parameters": {
            "type": "object",
            "properties": {
                "version_id": {"type": "string"},
                "usage_type": {
                    "type": "string",
                    "description": "e.g. advertisement, ott, movie, trailer, social_media",
                },
            },
            "required": ["version_id", "usage_type"],
        },
    },
    {
        "name": "get_alternative_recommendations",
        "description": "Suggest cleared alternative versions when the requested one isn't usable.",
        "parameters": {
            "type": "object",
            "properties": {
                "version_id": {"type": "string"},
            },
            "required": ["version_id"],
        },
    },
]


def run_agent(user_question: str, max_steps: int = 6) -> dict:
    """Runs the multi-step tool-calling loop. Returns final answer + trace."""
    client = genai.Client(api_key=os.environ["GOOGLE_API_KEY"])
    tool = types.Tool(function_declarations=_TOOL_DECLARATIONS)
    config = types.GenerateContentConfig(
        system_instruction=_SYSTEM_INSTRUCTION,
        tools=[tool],
    )

    contents = [types.Content(role="user", parts=[types.Part(text=user_question)])]
    trace = []

    for step in range(max_steps):
        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=contents,
            config=config,
        )
        candidate = response.candidates[0]
        contents.append(candidate.content)

        function_calls = [
            part.function_call for part in candidate.content.parts
            if part.function_call is not None
        ]

        if not function_calls:
            final_text = "".join(
                part.text for part in candidate.content.parts if part.text
            )
            return {"answer": final_text, "trace": trace, "steps_taken": step + 1}

        function_response_parts = []
        for fc in function_calls:
            fn = TOOL_REGISTRY.get(fc.name)
            if fn is None:
                result = {"error": f"unknown tool {fc.name}"}
            else:
                result = fn(**fc.args)

            trace.append({"tool": fc.name, "args": dict(fc.args), "result": result})
            function_response_parts.append(
                types.Part.from_function_response(name=fc.name, response=result)
            )

        contents.append(types.Content(role="user", parts=function_response_parts))

    return {
        "answer": "Agent did not converge to a final answer within step limit.",
        "trace": trace,
        "steps_taken": max_steps,
    }