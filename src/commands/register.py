from discord.ext import commands
import discord
from werkzeug.security import generate_password_hash
from db import create_user, get_user

class RegisterCommand(commands.Cog):  # ← ここを修正
    def __init__(self, bot):
        self.bot = bot
    
    async def ask_in_dm(self, user: discord.User, question: str, timeout: int = 60, hide: bool = False):
        """
        DMで質問を送り、ユーザーの返答を待つ。
        hide=True の場合、パスワードなどを隠すため即削除。
        """
        try:
            await user.send(question)

            def check(m):
                return m.author == user and isinstance(m.channel, discord.DMChannel)

            msg = await self.bot.wait_for("message", check=check, timeout=timeout)
            content = msg.content.strip()

            if hide:
                try:
                    await msg.delete()  # パスワードをログに残さないよう削除
                except discord.Forbidden:
                    pass

            return content
        except Exception:
            return None

    async def register_user(self, user: discord.User):
        # ユーザー名を取得
        username = await self.ask_in_dm(user, "登録するユーザー名を入力してください：")
        if not username:
            await user.send("タイムアウトしました。再度 `!register` を実行してください。")
            return

        # 重複チェック
        if get_user(username):
            await user.send("そのユーザー名は既に使用されています。別の名前を入力して再度 `!register` を実行してください。")
            return

        # パスワードを取得（表示を残さない）
        password = await self.ask_in_dm(user, "登録するパスワードを入力してください：", hide=True)
        if not password:
            await user.send("タイムアウトしました。再度 `!register` を実行してください。")
            return

        # ハッシュ化してDBに保存
        password_hash = generate_password_hash(password)
        create_user(username, password_hash)
        await user.send(f"ユーザー `{username}` を登録しました！")

    @commands.command(name="register")
    async def register(self, ctx):
        """DMでユーザー登録を行うコマンド"""
        try:
            await ctx.author.send("ユーザー登録を開始します。DMで案内します。")
        except discord.Forbidden:
            await ctx.send("DMを送信できませんでした。DMを受け取れる設定にしてください。")
            return

        # DMでやり取り開始
        await self.register_user(ctx.author)
        await ctx.send(f"{ctx.author.mention} 登録処理が完了しました（DMを確認してください）。")

async def setup(bot):
    await bot.add_cog(RegisterCommand(bot))
    print("RegisterCommand Cog loaded")