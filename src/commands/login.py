from discord.ext import commands
from werkzeug.security import check_password_hash
from db import get_user

class LoginCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logged_in_users = {}  # DiscordユーザーID: アプリ内ユーザーID

    @commands.command(name='login')
    async def login(self, ctx, username: str, password: str):
        user = get_user(username)
        if not user:
            await ctx.send("ユーザーが見つかりません。")
            return
        if check_password_hash(user[2], password):
            self.logged_in_users[ctx.author.id] = user[0]
            await ctx.send(f"{username} としてログインしました。")
        else:
            await ctx.send("パスワードが違います。")

    @commands.command(name='logout')
    async def logout(self, ctx):
        if ctx.author.id in self.logged_in_users:
            del self.logged_in_users[ctx.author.id]
            await ctx.send("ログアウトしました。")
        else:
            await ctx.send("ログインしていません。")

async def setup(bot):
    await bot.add_cog(LoginCommand(bot))