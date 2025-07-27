from discord.ext import commands

class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='shisha_help')  # ← コマンド名変更
    async def shisha_help(self, ctx):
        help_text = (
            "**シーシャ記録Discord Botの使い方**\n"
            "1. `!register`  … アプリからDMが届くのでそれに従ってユーザー登録を実施してください\n"
            "2. `!login ユーザー名 パスワード` … ログイン\n"
            "3. `!logout` … ログアウト\n"
            "4. `!add_log 日付 店名 メインフレーバー [サブ1] [サブ2] [サブ3] [サブ4] -- 感想`\n"
            "　　サブフレーバーは最大4つまで、`--`以降が感想です。\n"
            "5. `!show_logs` … 自分のシーシャログ一覧を表示（通し番号付き）\n"
            "6. `!delete_log 番号` … 指定した番号のログを削除\n"
            "\n"
            "※各コマンドはログイン後に利用できます。\n"
            "※サブフレーバーと感想の区切りには `--` を使用してください。\n"
            "※ログの削除は通し番号で指定します。\n"
        )
        await ctx.send(help_text)

async def setup(bot):
    await bot.add_cog(HelpCommand(bot))