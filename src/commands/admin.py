from discord.ext import commands
from src.db import delete_user_from_db
from discord import Embed

class AdminCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='delete_user')
    @commands.has_permissions(administrator=True)
    async def delete_user(self, ctx, user_id: int):
        result = delete_user_from_db(user_id)
        if result:
            await ctx.send(f'ユーザー {user_id} を削除しました。')
        else:
            await ctx.send(f'ユーザー {user_id} は存在しません。')

    @commands.command(name='admin_info')
    @commands.has_permissions(administrator=True)
    async def admin_info(self, ctx):
        embed = Embed(title="管理者コマンド", description="以下のコマンドが利用可能です。")
        embed.add_field(name="!delete_user <user_id>", value="指定したユーザーを削除します。", inline=False)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(AdminCommands(bot))