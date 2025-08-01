from discord.ext import commands
from db import get_shisha_logs, update_shisha_log
from discord import Embed

class EditLogCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='edit_log')
    async def edit_log(self, ctx, log_number: int):
        login_cog = self.bot.get_cog('LoginCommand')
        if not login_cog or ctx.author.id not in login_cog.logged_in_users:
            await ctx.send("先にログインしてください。")
            return
        user_id = login_cog.logged_in_users[ctx.author.id]
        logs = sorted(get_shisha_logs(user_id), key=lambda x: x[2])
        if not logs or log_number < 1 or log_number > len(logs):
            await ctx.send("指定した番号のログが見つかりません。")
            return
        log = logs[log_number - 1]
        log_id = log[0]

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        await ctx.send(f"新しい日付を入力してください（現在: {log[2]}、空欄なら変更なし）")
        date_msg = await self.bot.wait_for("message", check=check, timeout=60)
        date = date_msg.content.strip() or log[2]

        await ctx.send(f"新しい店名を入力してください（現在: {log[3]}、空欄なら変更なし）")
        shop_msg = await self.bot.wait_for("message", check=check, timeout=60)
        shop_name = shop_msg.content.strip() or log[3]

        await ctx.send(f"新しいメインフレーバーを入力してください（現在: {log[4]}、空欄なら変更なし）")
        main_msg = await self.bot.wait_for("message", check=check, timeout=60)
        main_flavor = main_msg.content.strip() or log[4]

        await ctx.send(f"新しいサブフレーバー（最大4つ、カンマ区切り、現在: {log[5]}、空欄なら変更なし）")
        sub_msg = await self.bot.wait_for("message", check=check, timeout=60)
        subs = [s.strip() for s in sub_msg.content.split(",") if s.strip()] if sub_msg.content.strip() else log[5].split(",")
        subs = subs[:4]
        sub_flavors = ','.join(subs)

        await ctx.send(f"新しい感想を入力してください（現在: {log[6]}、空欄なら変更なし）")
        comment_msg = await self.bot.wait_for("message", check=check, timeout=120)
        comment = comment_msg.content.strip() or log[6]

        try:
            update_shisha_log(log_id, date, shop_name, main_flavor, sub_flavors, comment)
            embed = Embed(
                title="シーシャログ修正",
                description=(
                    f"番号: {log_number}\n"
                    f"日付: {date}\n"
                    f"店名: {shop_name}\n"
                    f"メインフレーバー: {main_flavor}\n"
                    f"サブフレーバー: {sub_flavors}\n"
                    f"感想: {comment}\n"
                    "シーシャログが修正されました。"
                ),
                color=0x00ff00
            )
            await ctx.send(embed=embed)
        except Exception as e:
            embed = Embed(title="エラー", description=f"修正中にエラーが発生しました: {str(e)}", color=0xff0000)
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(EditLogCommand(bot))