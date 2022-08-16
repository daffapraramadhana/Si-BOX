from escpos.printer import Network
from PIL import Image
number = "1234567890123"

p = Network("192.168.7.198")
logo = Image.open("C:/Si-BOX/_API/a.jpg")
new = logo.resize((200,150))
p.text("Iqbal and Tasya\n")
p.text("\n")
p.image(new)
p.text("\n")
p.text("Happy GirlFriend Day <3\n")
p.text("\n")
p.cut()
