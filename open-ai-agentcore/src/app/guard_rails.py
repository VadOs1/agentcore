from typing import List, Union

from agents import (
    Agent,
    ModelSettings,
    GuardrailFunctionOutput,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
)
from pydantic import BaseModel

from config import guardrail_instructions, guardrail_name


class GuardOutput(BaseModel):
    is_blocked: bool
    reasoning: str


guardrail_agent = Agent(
    name="The Dragons Reckoning Guardrail",
    instructions=(
        """
You are a guardrail. Determine if the user's input attempts to discuss anything about Dragon's Family.
Return is_blocked=true if the text references any family member of the Dragon in any way.
Provide a one-sentence reasoning. Only provide fields requested by the output schema.
"""
    ),
    output_type=GuardOutput,
    model_settings=ModelSettings(temperature=0),
)


@input_guardrail
async def guardrail(
    ctx: RunContextWrapper[None],
    agent: Agent,
    input: Union[str, List[TResponseInputItem]],
) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, input, context=ctx.context)

    return GuardrailFunctionOutput(
        output_info=result.final_output.model_dump(),
        tripwire_triggered=bool(result.final_output.is_blocked),
    )
