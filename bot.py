import discord
from discord.ext import commands
import time
import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

BOT_TOKEN = os.getenv("DISCORD_TOKEN")
UNLOCK_CODE = "217"

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_health_server():
    port = int(os.getenv("PORT", 8080))
    server = HTTPServer(("0.0.0.0", port), HealthHandler)
    server.serve_forever()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.command()
async def speed(ctx, code: str = None):
    if code != UNLOCK_CODE:
        await ctx.send("اكتب `!speed 217` عشان يشتغل معك البوت.")
        return

    sent_at = ctx.message.created_at.timestamp() * 1000
    now = time.time() * 1000
    api_latency = bot.latency * 1000

    await ctx.send(
        f"**{ctx.author.display_name}**\n"
        f"زمن وصول رسالتك: **{now - sent_at:.0f} ms**\n"
        f"ping البوت للسيرفر: **{api_latency:.0f} ms**"
    )

threading.Thread(target=run_health_server, daemon=True).start()
bot.run(BOT_TOKEN)
