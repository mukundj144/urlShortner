import png 
import pyqrcode

class qr_code:
    def make_qr(self, url, special_key):        
        url = pyqrcode.create(url)
        url.png(special_key + ".png", scale=6)
