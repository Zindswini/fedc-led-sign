import os
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw

fs = open("/home/pi/welcome_banner.txt", "r")
contents = fs.read().split("\n")
fs.close()

text = []
for i in range(0, contents.__len__()-1, 2):
    text.append(tuple([contents[i], tuple(map(int, contents[i+1].split(" ")))]))
    #print(i)
 
text = tuple(text)
#print text

font = ImageFont.truetype("/home/pi/Desktop/FreeSans.ttf", 28)
all_text = ""
for text_color_pair in text:
    t = text_color_pair[0]
    all_text = all_text + t
 
print(all_text)
width, ignore = font.getsize(all_text)
#print(width)
 

im = Image.new("RGB", (width + 30, 32), "black")
draw = ImageDraw.Draw(im)
 
x = 0
for text_color_pair in text:
    t = text_color_pair[0]
    c = text_color_pair[1]
    #print("t=" + t + " " + str(c) + " " + str(x))
    draw.text((x, 0), t, c, font=font)
    x = x + font.getsize(t)[0]
 
im.save("banner.ppm")
