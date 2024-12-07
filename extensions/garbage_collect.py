import asyncio
import discord
from discord import app_commands
from discord.ext import commands
from daug.utils.dpyexcept import excepter
from daug.utils.dpylog import dpylogger


class GarbageCollectCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name='garbage_collect', description='サーバー内のTCから退出者のメッセージを全削除します')
    @app_commands.default_permissions(administrator=True)
    @app_commands.guild_only()
    @excepter
    @dpylogger
    async def _garbate_collect(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        notice = await interaction.followup.send('全TCのメッセージを確認中です', ephemeral=True)
        garbages: set[discord.Message] = set()
        users: set[discord.User] = set()
        for index, tc in enumerate(interaction.guild.text_channels):
            await notice.edit(embed=discord.Embed(
                description=f'{tc.mention} を確認中（{index}件目）\n削除対象メッセージ：{len(garbages)}件\n\n削除対象ユーザ\n{" ".join([u.mention for u in users])}',
            ))
            async for message in tc.history(limit=None):
                if message.author.bot:
                    continue
                if message.type is not discord.MessageType.default and message.type is not discord.MessageType.reply:
                    continue
                if message.webhook_id:
                    continue
                if isinstance(message.author, discord.User):
                    garbages.add(message)
                    users.add(message.author)
                    await message.delete()
                    await asyncio.sleep(1)
        await notice.edit(content='全TCのメッセージの確認が完了しました', embed=discord.Embed(
            description=f'削除対象メッセージ：{len(garbages)}件\n\n削除対象ユーザ\n{" ".join([u.mention for u in users])}',
        ))


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(GarbageCollectCog(bot))
