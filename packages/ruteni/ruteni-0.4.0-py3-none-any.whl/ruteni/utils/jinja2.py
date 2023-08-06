from typing import Any

from anyio import open_file

import jinja2


async def render_template(template_path: str, params: dict[str, Any]) -> str:
    "Render a template using Jinja2"
    async with await open_file(template_path) as f:
        content = await f.read()
    template = jinja2.Template(content, enable_async=True)  # type: ignore
    return await template.render_async(params)
