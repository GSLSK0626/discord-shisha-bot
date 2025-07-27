from discord.ext import commands
from db import get_shisha_logs, delete_shisha_log
from discord import Embed

class DeleteLogCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='delete_log')
    async def delete_log(self, ctx, log_number: int):
        # DiscordユーザーIDからアプリ内ユーザーIDを取得
        login_cog = self.bot.get_cog('LoginCommand')
        if not login_cog or ctx.author.id not in login_cog.logged_in_users:
            await ctx.send("先にログインしてください。")
            return
        user_id = login_cog.logged_in_users[ctx.author.id]
        logs = sorted(get_shisha_logs(user_id), key=lambda x: x[2])  # x[2]はdate
        if not logs or log_number < 1 or log_number > len(logs):
            await ctx.send("指定した番号のログが見つかりません。")
            return
        log_id = logs[log_number - 1][0]  # 通し番号からDBのIDを取得
        try:
            delete_shisha_log(log_id)
            embed = Embed(
                title="シーシャログ削除",
                description=f"番号 {log_number} のログを削除しました。",
                color=0xff0000
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = Embed(title="エラー", description=f"削除中にエラーが発生しました: {str(e)}", color=0xff0000)
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(DeleteLogCommand(bot))