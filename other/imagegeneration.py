from PIL import Image, ImageDraw, ImageOps

class ImageGenerator():

    @classmethod
    def generate_level_card(cls, uesrname, level, rank, xp):
        card = Image.new("RGBA", (int(412*2*1.25), int(412*1.25)), (255, 255, 255, 255)) 
        pfp = Image.open('other/average_discord_user_pfp.png')
        pfp = pfp.resize((212, 212))
        
        # mask
        mask = Image.new("L", (212, 212), 0) 
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, 212, 212), fill=255)  

        pfp.putalpha(mask) 

        card.paste(pfp, (50, 50), pfp)
        draw = ImageDraw.Draw(card)
        draw.text((262+16,50),'Hello World',fill=0x000000)


        card.save('img.png')
