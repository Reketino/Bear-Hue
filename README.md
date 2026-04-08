# Bear-Hue

A simple app for controlling my Philips Hue lights from my computer🔦

---

### Learning Aspect:

- Learning how to connect to and control smart home devices through the Philips Hue API
- Learning how to work with APIs that interact with real-world electronics
- Building software applications for practical, real-world use

---

###  Current Status:

- ✅ Desktop UI working
- ✅ Scene system with color preview
- ✅ Hue API integration
- ✅ EXE build working

---

### Future plans:

- PC application w/ settings
- UI for controlling lights
- Button for turning on/off lights
- Setting up different light modes
- "Bear Mode" UI toggle

---

### Setup

1. Create a developer account  
https://developers.meethue.com/develop/hue-api-v2/getting-started/

2. Find your bridge IP  
https://discovery.meethue.com/

3. Press the button on your Hue Bridge

4. Within 30 seconds run:

```
bash
curl -X POST http://<HUE_BRIDGE_IP>/api \
-H "Content-Type: application/json" \
-d '{"devicetype":"bear_hue_app"}'
```
---

### Tech Stack:

- Python 3.12
- CustomTkinter
- Pillow
- Requests
- Philips Hue API

---

### 🟢 Working on:

- Adding get bear color to change brightness

---

### Run Scripts:

----

## Test for Philips Hue connection: 
python -m tests.test_api

## Test for Philips Hue Service: 
python -m tests.test_service

----

## Main Script to turn lights on/off:
python -m src.scripts.main 

---


