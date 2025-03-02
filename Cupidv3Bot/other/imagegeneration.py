from PIL import Image, ImageDraw, ImageOps, ImageFont
from io import BytesIO
import requests

class ImageGenerator():

    @classmethod
    def generate_level_card(cls, user_id, uesrname, avatar_url, level, xp, rank):
        # create card, get pfp, size it.
        card = Image.new("RGBA", (int(1440), int(350)), (0, 0, 0, 0))
        draw = ImageDraw.Draw(card)
        draw.rounded_rectangle([0,0,1440,515], fill=0xffa6a1ff,radius=50)
        r = requests.get(avatar_url)

        pfp = Image.open(BytesIO(r.content))
        pfp = pfp.resize((212, 212))
        
        # create a mask to make the pfp circular
        mask = Image.new("L", (212, 212), 0) 
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, 212, 212), fill=255)  
        
        pfp.putalpha(mask)
        card.paste(pfp, (50, 50), mask)
        
        draw = ImageDraw.Draw(card)

        arial_bold_90 = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', size=90)
        arial_75 = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', size=75)
        arial_40 = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', size=40)

        draw.text((262+16,50),uesrname,fill=0x000000, font=arial_bold_90)
        draw.text((262+16,160),f'Level: {level} Rank: {rank}',fill=0x000000, font=arial_75)
        #draw.text((262+16,200),f'Rank: {rank}',fill=0x000000, font=arial_75)

        base_top_left = (50, 275)
        base_bottom_right = (1390, 275+50)

        xp_required = level*100
        xp_percentage = xp/xp_required
        xp_progess = (int(1387*xp_percentage), 275+50-3)

        xp_top_left = (53, 275+3)
        xp_bottom_right = (113, 275+50-3)



        
        draw.rounded_rectangle([base_top_left, base_bottom_right], radius=25, fill=0xffa1a1a1, outline=00000000, width=3)
        if xp_progess[0] < 113: draw.rounded_rectangle([xp_top_left, xp_bottom_right], radius=25, fill=0xffcd1aff)
        else: draw.rounded_rectangle([xp_top_left, xp_progess], radius=25, fill=0xffcd1aff)
        draw.text((1440/2,300), f"XP: {xp}/{level*100}", font=arial_40, fill=0x000000, align='center', anchor="mm")
        


        card.save(f'images/{user_id}.png')
