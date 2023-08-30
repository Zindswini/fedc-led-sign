import subprocess
import os
import signal
from flask import Flask, render_template, request
from PIL import ImageFont, Image, ImageDraw

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    message = None

    if request.method == 'POST':
        entered_text = request.form['textbox']
        print("Text entered:", entered_text)

        # Try to update display
        if entered_text:
            try:
                generatePPT(buildMessage(entered_text), "./font/Quicksilver.ttf")

                # If the ppt generation was successful, write new text to file
                writeFile(entered_text)
                restart_display_process()
                message = "Success: Sign regenerated, process restarted"
                            
            except Exception as e:
                message = e # print exception to web
        else:
            message = "Failure: Please enter text."

    default_text = readFile()

    return render_template('index.html', message=message, default_text=default_text)

def readFile():
    fs = open("./welcome_banner.txt", "r")
    contents = fs.read()
    fs.close()
    return contents

def writeFile(contents):
    fs = open("./welcome_banner.txt", "w")
    fs.write(contents)
    fs.close()


# convert the message text into a tuple of (text, [r,g,b]) values
def buildMessage(contents):
    tmptext = []
    contents = contents.split("\n")

    for i in range(0, contents.__len__()-1, 2):
        tmptext.append(tuple([contents[i], tuple(map(int, contents[i+1].split(" ")))]))
    return tmptext


def generatePPT(message, fontpath):
    font = ImageFont.truetype(fontpath,28)

    all_text = ""
    for text_color_pair in message:
        t = text_color_pair[0]
        all_text = all_text + t

    width = int(font.getlength(all_text))
    #width, ignore = font.getsize(all_text)

    im = Image.new("RGB", (width + 30, 32), "black")
    draw = ImageDraw.Draw(im)
 
    x = 0
    for text_color_pair in message:
        t = text_color_pair[0]
        c = text_color_pair[1]
        #print("t=" + t + " " + str(c) + " " + str(x))
        draw.text((x, 0), t, c, font=font)
        #print(font.getlength(t))
        x = x + int(font.getlength(t))
        #x = x + font.getsize(t)[0]
 
    im.save("banner.ppm")

def start_display_process():
    process = subprocess.Popen(["taskset", "3", "../rpi-rgb-led-matrix/examples-api-use/demo", "--led-rows=32", "--led-chain=10", "--led-brightness=75", "--led-gpio-mapping=adafruit-hat-pwm", "-m", "10", "-D", "1", "./banner.ppm"], shell=False, preexec_fn=os.setpgrp)
    with open("./process_pid.txt", "w") as f:
        f.write(str(process.pid))
    return process

def get_display_process_pid():
    if os.path.exists("./process_pid.txt"):
        with open("./process_pid.txt", "r") as f:
            return int(f.read())
    return None

def restart_display_process():
    old_pid = get_display_process_pid()
    if old_pid:
        try:
            os.killpg(old_pid, signal.SIGTERM)
            os.waitpid(old_pid, 0)
        except ProcessLookupError:
            pass  # Process is already terminated
    new_process = start_display_process()
    return new_process

if __name__ == '__main__':
    display_process = start_display_process()
    app.run(host="0.0.0.0", debug=True)