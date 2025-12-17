import nextcord
from nextcord.ext import commands
import requests, datetime

TOKEN = ""
CARD_IMAGE_URL = "https://i.pinimg.com/originals/0a/d7/35/0ad735f722522d9a424b2a018ff63319.gif"
API_URL = "https://netflix.gafiwshop.xyz/disney.php?mode=json&email=qbnjfcaa193%40sell24hr.xyz&ts=1765292730183"

bot = commands.Bot(intents=nextcord.Intents.default())

class UIOTPView(nextcord.ui.View):
    def __init__(self): super().__init__(timeout=None)

    @nextcord.ui.button(label="ดึง OTP", style=nextcord.ButtonStyle.primary)
    async def fetch_otp(self, _, it: nextcord.Interaction):
        await it.response.defer(ephemeral=True)
        try:
            data = requests.get(API_URL, timeout=10).json()
            print(data) 

            emails = data.get("emails") or []
            if data.get("status") != "success" or not emails:
                print("OTP NOT FOUND", it.user)
                return await it.followup.send("ไม่พบ OTP", ephemeral=True)

            m = emails[0]
            name, otp = m.get("name", "-"), m.get("otp", "-")
            print(it.user, name, otp) 

            emb = nextcord.Embed(
                title="OTP ล่าสุด",
                description=f"**บริการ:** {name}\n**OTP:** ` {otp} `",
                color=nextcord.Color.blurple()
            )
            emb.set_image(url=CARD_IMAGE_URL)
            emb.set_footer(text=f"เรียกโดย {it.user}", icon_url=it.user.display_avatar.url)
            emb.timestamp = datetime.datetime.now()

            await it.followup.send(embed=emb, ephemeral=True)

        except Exception as e:
            print("ERROR:", e)
            await it.followup.send("ระบบผิดพลาด", ephemeral=True)

@bot.slash_command(name="uiotp", description="แสดง UI ดึง OTP (ถาวร)")
async def uiotp(it: nextcord.Interaction):
    emb = nextcord.Embed(
        title="ดึง OTP",
        description="กดปุ่มด้านล่างเพื่อดึง OTP ล่าสุด",
        color=nextcord.Color.dark_gray()
    )
    emb.set_image(url=CARD_IMAGE_URL)
    await it.send(embed=emb, view=UIOTPView())

@bot.event
async def on_ready():
    bot.add_view(UIOTPView())
    print("BOt User:", bot.user)

bot.run(TOKEN)
