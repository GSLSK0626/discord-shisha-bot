from discord.ext import commands

async def setup_commands(bot):
    from .register import setup as register_setup
    from .login import setup as login_setup
    from .add_log import setup as add_log_setup
    from .delete_log import setup as delete_log_setup
    from .show_logs import setup as show_logs_setup
    from .help import setup as help_setup  # ← 追加
    await register_setup(bot)
    await login_setup(bot)
    await add_log_setup(bot)
    await delete_log_setup(bot)
    await show_logs_setup(bot)
    await help_setup(bot)  # ← 追加