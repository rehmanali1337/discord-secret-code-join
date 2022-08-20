from discord.ext import commands
import discord
import asyncio
import config
from app import md, gvs
from app.state import State
import typing


class HaveCodeMenu:
    YES = "Yes"
    NO = "No"
    ID = "have_code_menu"

    @classmethod
    def get_menu(cls, author: discord.Member = None):
        options = [
            discord.SelectOption(cls.YES, value=cls.YES, description="Have secret code"),
            discord.SelectOption(cls.NO, value=cls.NO, description="Don't have secret code")
        ]
        menu = discord.SelectMenu(cls.ID, options=options)
        prompt = "Do you have a secret code?"
        if author is not None:
            prompt = f"{author.mention} {prompt}"
        return menu, md.line_embed(prompt)


class CodeJoin(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot: commands.Bot = bot
        self.codes_channel_id = config.CODE_CHANNEL_ID
        self.codes_channel: discord.TextChannel = self.bot.get_channel(self.codes_channel_id)
        if not self.codes_channel:
            raise RuntimeError("Codes channel not found.")
        asyncio.create_task(self.setup())

    async def setup(self):
        """Run at the startup in the background to setup the channels."""
        await self.clear_channel(self.codes_channel)
        components, prompt = HaveCodeMenu.get_menu()
        await self.codes_channel.send(embed=prompt, components=components)

    @commands.Cog.on_select(custom_id=HaveCodeMenu.ID)
    async def on_code_menu_selection(self, intr: discord.Interaction, selected: discord.SelectMenu):
        """When user selects a menu option"""
        await intr.defer(hidden=True)
        selected = selected.values[0]
        if selected == HaveCodeMenu.YES:
            await intr.respond(f"{intr.author.mention} Please send us the secret code you have?", hidden=True)
            code_message = await self._get_user_input(intr.author, intr.channel)
            secret_code = code_message.content.strip()
            try:
                await code_message.delete()
            except:
                pass
            if secret_code not in State.codes:
                e = md.line_embed(f"{intr.author.mention} Invalid code.")
                return await intr.respond(embed=e, hidden=True)
            if secret_code in State.codes:
                await State.mark_code_used(secret_code)
                # TODO: Assign role now
                await self.assign_role(intr.author, config.SPECIAL_ROLE_ID)
                e = md.line_embed(f"{intr.author.mention} You have got the special role.")
                return await intr.respond(embed=e, hidden=True)
        if selected == HaveCodeMenu.NO:
            e = md.line_embed("Thank you.")
            return await intr.respond(embed=e, hidden=True)

    async def _get_user_input(self, member: discord.Member, channel: discord.TextChannel) -> discord.Message:

        def check(m):
            return m.channel == channel and m.author == member

        return await self.bot.wait_for("message", check=lambda m: check(m), timeout=gvs.DEFAULT_EVENT_TIMEOUT)

    async def assign_role(self, member: discord.Member, role: typing.Union[int, discord.Role]):
        if isinstance(role, int):
            role = discord.utils.get(member.guild.roles, id=role)
        if isinstance(role, discord.Role):
            await member.add_roles(role)

    async def clear_channel(self, channel: discord.TextChannel):
        """Clear all messages from channel."""
        to_del = []
        async for m in channel.history():
            to_del.append(m)
            if len(to_del) == 100:
                try:
                    await channel.delete_messages(to_del)
                except:
                    pass

        async def _del(m):
            try:
                await m.delete()
            except:
                pass

        tasks = []
        async for m in channel.history():
            tasks.append(asyncio.create_task(_del(m)))
            if len(tasks) == 5:
                await asyncio.gather(*tasks)


def setup(bot: commands.Bot):
    bot.add_cog(CodeJoin(bot))
    print("CodeJoin extesnsion loaded!")
