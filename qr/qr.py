import os
import qrcode

img = qrcode.make("https://www.theknot.com/us/ashton-creel-and-jay-broussard-nov-2025")

img.save("qr.png", "PNG")
