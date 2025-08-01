from discord.ext import commands
from db import add_shisha_log
from discord import Embed

class AddLogCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='add_log')
    async def add_log(self, ctx):
        login_cog = self.bot.get_cog('LoginCommand')
        if not login_cog or ctx.author.id not in login_cog.logged_in_users:
            await ctx.send("先にログインしてください。")
            return
        user_id = login_cog.logged_in_users[ctx.author.id]

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        # 日付
        await ctx.send("日付を入力してください（例: 2025-07-21）")
        date_msg = await self.bot.wait_for("message", check=check, timeout=60)
        date = date_msg.content.strip()

        # 店名
        await ctx.send("店名を入力してください")
        shop_msg = await self.bot.wait_for("message", check=check, timeout=60)
        shop_name = shop_msg.content.strip()

        # メインフレーバー
        await ctx.send("メインフレーバーを入力してください")
        main_msg = await self.bot.wait_for("message", check=check, timeout=60)
        main_flavor = main_msg.content.strip()

        # サブフレーバー（最大4つまで、カンマ区切りで入力）
        await ctx.send("サブフレーバーを最大4つまでカンマ区切りで入力してください（例: グレープ,ミント,レモン）")
        sub_msg = await self.bot.wait_for("message", check=check, timeout=60)
        subs = [s.strip() for s in sub_msg.content.split(",") if s.strip()]
        subs = subs[:4]
        sub_flavors = ','.join(subs)

        # 感想
        await ctx.send("感想を入力してください（任意、空欄でもOK）")
        comment_msg = await self.bot.wait_for("message", check=check, timeout=120)
        comment = comment_msg.content.strip()

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