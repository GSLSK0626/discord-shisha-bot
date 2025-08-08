from discord.ext import commands

class HelpCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='shisha_help')
    async def shisha_help(self, ctx):
        help_text = (
            "**シーシャ記録Discord Botの使い方**\n"
            "1. `!register`  … アプリからDMが届くのでそれに従ってユーザー登録を実施してください\n"
            "2. `!login ユーザー名 パスワード` … ログイン\n"
            "3. `!logout` … ログアウト\n"
            "4. `!add_log` … Botの案内に従い、インタラクティブにシーシャログを登録\n"
            "5. `!show_logs` … 自分のシーシャログ一覧を表示（古い順に通し番号付き）\n"
            "6. `!delete_log 番号` … `!show_logs` で表示された通し番号のログを削除\n"
            "7. `!edit_log 番号` … 指定した通し番号のログをインタラクティブに修正\n"
            "8. `!search_flavor フレーバー名` … 指定したフレーバー名を含むログを検索\n"
            "\n"
            "※各コマンドはログイン後に利用できます。\n"
            "※サブフレーバーは最大4つまで、カンマ区切りで入力します。\n"
            "※ログの削除・修正は通し番号で指定します。\n"
            "※フレーバー検索はメイン・サブ両方が対象です。\n"
        )
        await ctx.send(help_text)

async def setup(bot):
    await bot.add_cog(HelpCommand(bot))