import hashlib, requests, websocket,json, time, random
import _thread as thread
def genToken(username, passwd):
    return requests.get("https://api.valiantmc.net/i/auth", params={
        "user": username,
        "password": hashlib.sha1(
            "VALIANTMC.NET[{}]".format(passwd).encode("utf-8")
            ).hexdigest().upper()
        })
username = "[URURSERNAME]"
token = genToken("[URURSERNAME]", "PASSWORD").json()["token"]
def on_message(ws, message):
    handle_message(ws, message)

def find_username(message):
    try: return json.loads(json.loads(message)['rawJson'])["extra"][6]["text"]
    except: return None
def isConnected(message):
    try:
        if json.loads(json.loads(message)['rawJson'])["extra"][2]["text"] == "+": return json.loads(json.loads(message)['rawJson'])["extra"][5]["text"]
        else: return False

    except: return False
def isFriendRequest(message):
    try:
        if json.loads(json.loads(message)['rawJson'])["extra"][1]["text"] == "[✔] ": return json.loads(json.loads(message)['rawJson'])["extra"][1]["clickEvent"]["value"]
        else: return False
    except: return False
def send_message(text):
    objToSend = {
            "type": "input",
            "input": text
            }
    print(objToSend)
    ws.send(json.dumps(objToSend))

def getText(message):
    try: return json.loads(json.loads(message)['rawJson'])["extra"][7]["text"]
    except: return None

def handle_message(ws, message):
    conn = isConnected(message)
    welcomePresets = {
        "VoidCrafted": "Master, oh thy master, welcome back!",
        "ImAJesp": "Good day to you, ImAJesp",
        "Phooble": "I ship PhoobChipPlanet",
        "Myles": "Hey Myles! I am a new server bot. If VoidCrafted is on, ask him about me",
        "Tr♪s": "Does anyone smell something? Oh, Tris has joined xD",
        "TycerX": "Hey Tycer, I'm a bot!!",
        "Firework": "Hi _Firework",
        "AwesomeL2": "Hi L2!!!"}
    if conn != False:
        try: msg = welcomePresets[conn]
        except: msg = " Welcome back, {un}".format(un = conn)
        time.sleep(0.5)
        send_message(msg)
    fr = isFriendRequest(message)
    if fr != False:
        send_message(fr)
        
def on_open(ws):
    ws.send(json.dumps({"type": "auth","username": username,"token": token}))
    def run(*args):
        print(" ] Thread Spawned ")
        time.sleep(1)
        ws.send("{{\"type\": \"ping\", \"ping\": {ping}}}".format(ping = time.time()*1000))
        thread.start_new_thread(run, ())
        print(" ] Thread died ")
    thread.start_new_thread(run, ())
def on_error(ws, error):
    pass
def on_close(ws):
    print("closed")
if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://api.valiantmc.net/chat/",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()
