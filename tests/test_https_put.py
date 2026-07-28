import os
from pathlib import Path

from dotenv import load_dotenv

from src.api.hue_https import HueHTTPS


load_dotenv()


CA_BUNDLE = (
    Path(__file__).resolve().parents[1]
    / "src"
    / "assets"
    / "certificates"
    / "huebridge_cacert_bundle.pem"
)


def run_test():
    bridge_ip = os.getenv("HUE_BRIDGE_IP")
    bridge_id = os.getenv("HUE_BRIDGE_ID")
    username = os.getenv("HUE_USERNAME")

    if not bridge_ip:
        raise ValueError("HUE_BRIDGE_IP not found")

    if not bridge_id:
        raise ValueError("HUE_BRIDGE_ID not found")

    if not username:
        raise ValueError("HUE_USERNAME not found")

    hue = HueHTTPS(
        bridge_ip=bridge_ip,
        bridge_id=bridge_id,
        ca_bundle=str(CA_BUNDLE),
    )

    light = hue.get(
        f"/api/{username}/lights/1"
    )

    current_state = light["state"]["on"]

    print("Current state:", current_state)

    result = hue.put(
        f"/api/{username}/lights/1/state",
        payload={
            "on": current_state,
        },
    )

    print("PUT response:", result)
    print("\nSecure HTTPS PUT successful!")


if __name__ == "__main__":
    run_test()