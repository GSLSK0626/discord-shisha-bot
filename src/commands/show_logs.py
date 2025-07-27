from discord.ext import commands
from db import get_shisha_logs
from discord import Embed

class ShowLogsCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='show_logs')
    async def show_logs(self, ctx):
        # DiscordユーザーIDからアプリ内ユーザーIDを取得
        login_cog = self.bot.get_cog('LoginCommand')
        if not login_cog or ctx.author.id not in login_cog.logged_in_users:
            await ctx.send("先にログインしてください。")
            return
        user_id = login_cog.logged_in_users[ctx.author.id]
        logs = get_shisha_logs(user_id)
        if not logs:
            await ctx.send("ログがありません。")
            return
        embed = Embed(title="あなたのシーシャログ一覧", color=0x00bfff)
        for idx, log in enumerate(sorted(logs, key=lambda x: x[2]), start=1):  # x[2]はdate
            embed.add_field(
                name=f"番号: {idx} | {log[2]} | {log[3]}",
                value=f"メイン: {log[4]} / サブ: {log[5]}\n感想: {log[6]}",
                inline=False
            )
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ShowLogsCommand(bot))