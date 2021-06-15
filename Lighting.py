try:
  import usocket as socket
except:
  import socket

import machine
import network
import esp
esp.osdebug(None)
import neopixel
import time

import gc

# Clean up Memory, and print Version
gc.collect()
VersionNum ="0.70"
print("Version{0}".format(VersionNum))

# Define the buttons that will be displayed in the web interface.
# Button Name (and content flag), Function to run, function variables (singlecolor takes 3, but a different function may take more or none).
buttons = [["Red", "SingleColor", 10, 0, 0],
           ["Blue", "SingleColor", 0, 0, 10],
           ["Green", "SingleColor", 0, 10, 0],
           ["Yellow", "SingleColor", 10, 10, 0],
           ["Purple", "SingleColor", 10, 0, 10],
           ["Orange", "SingleColor", 10, 2, 0],
           ["Off", "SingleColor", 0,0,0]]

# Web server settings
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

#Neo Pixel Settings
StringLen = 26
StringPin = 14
PauseLen = 200

# Light settings
LightState = "OFF"
LightName = "Grill Light"


# Functions

def SingleColor(StringLen, StringPin, RVal, GVal, BVal):
    np = neopixel.NeoPixel(machine.Pin(StringPin), StringLen)
    for i in range(StringLen):
        np[i] = (int(RVal), int(GVal), int(BVal))
    np.write()

def HTMLPage():
    print("Rendering HTMLPage")

    html_head = """<html><head> <title>Lighting Control</title> <meta name="viewport" content="width=device-width, initial-scale=1">
      <link rel="icon" href="data:,"> <style>html{font-family: Helvetica; display:inline-block; margin: 0px auto; text-align: center;}
      h1{color: #0F3376; padding: 2vh;}p{font-size: 1.5rem;}.button{display: inline-block; background-color: #e7bd3b; border: none;
      border-radius: 4px; color: white; padding: 16px 40px; text-decoration: none; font-size: 30px; margin: 2px; cursor: pointer;}
      .button2{background-color: #4286f4;}</style></head><body>
      <h1>""" + LightName + """</h1>
      <p>Lighting state: <strong>""" + LightState + """</strong> Version """ + VersionNum + """</p>"""
    html_buttons ="""<br>\n"""
    for bnum in range(len(buttons)):
        html_buttons += """<p><a href="/?np="""+ buttons[bnum][0] +""""><button class="button">"""+ buttons[bnum][0]+"""</button></a></p>\n"""
    html_end = """</body></html>"""

    html = ''.join([html_head, html_buttons, html_end])
    return html


# Main

while True:
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    request = str(request)
    print('Content = %s' % request)
    for bnum in range(len(buttons)):
        rstring = '/?np={0}'.format(buttons[bnum][0])
        if request.find(rstring) == 6:
            print ('{0}: Selected via web'.format(rstring))
            if buttons[bnum][1] == "SingleColor":
                LightState = buttons[bnum][0]
                SingleColor(StringLen, StringPin, buttons[bnum][2], buttons[bnum][3], buttons[bnum][4])
            else:
                print("Invalid string: {0}".format(rstring))

    print("Start Web Render")
    response = HTMLPage()
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    conn.close()