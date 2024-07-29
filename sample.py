from datetime import datetime


date=datetime.now().strftime("%Y-%m-%d")
h=int(datetime.now().strftime("%H"))-6

print (date,h)