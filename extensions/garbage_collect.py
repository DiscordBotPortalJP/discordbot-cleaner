import asyncio
import datetime
import discord
from discord import app_commands
from discord.ext import commands
from daug.utils.dpyexcept import excepter
from daug.utils.dpylog import dpylogger


def compose_embeds(garbages, channels, users):
    embeds = [
        discord.Embed(
            title='削除対象メッセージ',
            description=f'{len(garbages)}件',
        ),
        discord.Embed(
            title='削除対象チャンネル',
            description=f'{" ".join([c.mention for c in channels])}',
        ),
        discord.Embed(
            title='削除対象ユーザ',
            description=f'{" ".join([u.mention for u in users])}',
        ),
    ]
    return embeds    


class GarbageCollectCog(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name='テキストチャンネルの整理', description='サーバー内のTCから退出者のメッセージを全削除します')
    @app_commands.default_permissions(administrator=True)
    @app_commands.guild_only()
    @excepter
    @dpylogger
    async def _garbate_collect_textchannel(self, interaction: discord.Interaction):
        await interaction.response.send_message('サーバー内のTCから退出者のメッセージを全削除します', ephemeral=True)
        notice = await interaction.channel.send('全TCのメッセージを確認中です')
        garbages: set[discord.Message] = set()
        channels: set[discord.TextChannel] = set()
        users: set[discord.User] = set()
        fourteen_days_ago = datetime.datetime.now() - datetime.timedelta(days=14)
        for index, tc in enumerate(interaction.guild.text_channels):
            await notice.edit(
                content=f'{tc.mention} を確認中（{index}件目）',
                embeds=compose_embeds(garbages, channels, users),
            )
            async for message in tc.history(limit=None, after=fourteen_days_ago):
                if message.author.bot:
                    continue
                if message.type is not discord.MessageType.default and message.type is not discord.MessageType.reply:
                    continue
                if message.webhook_id:
                    continue
                if isinstance(message.author, discord.User):
                    garbages.add(message)
                    channels.add(channels)
                    users.add(message.author)

        delete_count = 0
        for channel in channels:
            await notice.edit(content=f'メッセージを削除中です（{delete_count}/{len(garbages)}件完了）')
            delete_messages = [m for m in garbages if m.channel.id == channel.id]
            await channel.delete_messages(delete_messages)
            delete_count += len(delete_messages)

        # for index, message in enumerate(garbages):
        #     if index % 10 == 0:
        #         await notice.edit(content=f'メッセージを削除中です（{index}/{len(garbages)}件完了）')
        #     await message.delete()
        #     await asyncio.sleep(1)

        await notice.edit(content='メッセージの削除が完了しました')

    @app_commands.command(name='ボイスチャンネルを整理', description='サーバー内のVCから退出者のメッセージを全削除します')
    @app_commands.default_permissions(administrator=True)
    @app_commands.guild_only()
    @excepter
    @dpylogger
    async def _garbate_collect_voicechannel(self, interaction: discord.Interaction):
        await interaction.response.send_message('サーバー内のVCから退出者のメッセージを全削除します', ephemeral=True)
        notice = await interaction.channel.send('全TCのメッセージを確認中です')
        garbages: set[discord.Message] = set()
        channels: set[discord.VoiceChannel] = set()
        users: set[discord.User] = set()
        fourteen_days_ago = datetime.datetime.now() - datetime.timedelta(days=14)
        for index, tc in enumerate(interaction.guild.text_channels):
            await notice.edit(
                content=f'{tc.mention} を確認中（{index}件目）',
                embeds=compose_embeds(garbages, channels, users),
            )
            async for message in tc.history(limit=None, after=fourteen_days_ago):
                if message.author.bot:
                    continue
                if message.type is not discord.MessageType.default and message.type is not discord.MessageType.reply:
                    continue
                if message.webhook_id:
                    continue
                if isinstance(message.author, discord.User):
                    garbages.add(message)
                    channels.add(channels)
                    users.add(message.author)

        delete_count = 0
        for channel in channels:
            await notice.edit(content=f'メッセージを削除中です（{delete_count}/{len(garbages)}件完了）')
            delete_messages = [m for m in garbages if m.channel.id == channel.id]
            await channel.delete_messages(delete_messages)
            delete_count += len(delete_messages)

        # for index, message in enumerate(garbages):
        #     if index % 10 == 0:
        #         await notice.edit(content=f'メッセージを削除中です（{index}/{len(garbages)}件完了）')
        #     await message.delete()
        #     await asyncio.sleep(1)

        await notice.edit(content='メッセージの削除が完了しました')


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(GarbageCollectCog(bot))
