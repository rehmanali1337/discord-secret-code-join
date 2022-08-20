

from __future__ import annotations
import discord


def code(text: str):
    return f"```{text}```"


def one_line_code(text: str):
    return f"`{text}`"


def highlight(text: str):
    return f"`{text}`"


def green_txt(text: str):
    return f"```css green text\n{text}```"


def line_embed(text: str, color=None):
    if not color:
        color = discord.Color.teal()
    e = discord.Embed(description=text)
    e.color = color
    return e


def bold(text: str):
    return f"***{text}***"
