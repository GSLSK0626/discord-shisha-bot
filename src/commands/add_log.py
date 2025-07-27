from discord.ext import commands
from db import add_shisha_log
from discord import Embed

class AddLogCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='add_log')
    async def add_log(self, ctx, date: str, shop_name: str, main_flavor: str, *args):
        # DiscordユーザーIDからアプリ内ユーザーIDを取得
        login_cog = self.bot.get_cog('LoginCommand')
        if not login_cog or ctx.author.id not in login_cog.logged_in_users:
            await ctx.send("先にログインしてください。")
            return
        user_id = login_cog.logged_in_users[ctx.author.id]
        # 区切り文字 '--' で分割
        if '--' in args:
            sep_index = args.index('--')
            subs = list(args[:sep_index])[:4]
            comment = ' '.join(args[sep_index+1:])
        else:
            subs = list(args[:4])
            comment = ' '.join(args[4:]) if len(args) > 4 else ''
        sub_flavors = ','.join(subs)
        try:
            add_shisha_log(user_id, date, shop_name, main_flavor, sub_flavors, comment)
            embed = Embed(
                title="シーシャログ追加",
                description=(
                    f"日付: {date}\n"
                    f"店名: {shop_name}\n"
                    f"メインフレーバー: {main_flavor}\n"
                    f"サブフレーバー: {sub_flavors}\n"
                    f"感想: {comment}\n"
                    "シーシャログが正常に追加されました。"
                ),
                color=0x00ff00
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = Embed(title="エラー", description=f"ログの追加中にエラーが発生しました: {str(e)}", color=0xff0000)
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(AddLogCommand(bot))