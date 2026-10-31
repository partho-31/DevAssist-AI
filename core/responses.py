"""Render chat strings and custom-parser results as conversation text."""
from pydantic import BaseModel


CODE_FIELDS = {"fixed_code", "corrected_code", "generated_code", "optimized_code"}


def format_response(response):
    if not isinstance(response, BaseModel):
        return str(response)

    parts = []
    for field, value in response.model_dump().items():
        if value is None or value == [] or value == "":
            continue
        title = field.replace("_", " ").title()
        if field in CODE_FIELDS:
            fence = "```"
            while fence in value:
                fence += "`"
            content = f"{fence}\n{value}\n{fence}"
        elif isinstance(value, list):
            content = "\n".join(f"- {item}" for item in value)
        else:
            content = str(value)
        parts.append(f"### {title}\n\n{content}")
    return "\n\n".join(parts)
