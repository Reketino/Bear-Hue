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

    data = hue.get(
        "/clip/v2/resource/scene",
        headers={
            "hue-application-key": username,
        },
    )

    scenes = data.get("data", [])

    print("\nSecure HTTPS connection successful!")
    print(f"Found {len(scenes)} V2 scenes.")

    for scene in scenes:
        metadata = scene.get("metadata", {})
        print("-", metadata.get("name", "Unknown"))


if __name__ == "__main__":
    run_test()