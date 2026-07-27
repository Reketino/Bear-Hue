import os
import socket
import ssl
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


CA_BUNDLE = (
    Path(__file__).resolve().parents[1]
    / "src"
    / "assets"
    / "certificates"
    / "huebridge_cacert_bundle.pem"
)


def test_tls():
    bridge_ip = os.getenv("HUE_BRIDGE_IP")
    bridge_id = os.getenv("HUE_BRIDGE_ID")

    if not bridge_ip:
        raise ValueError("HUE_BRIDGE_IP not found")

    if not bridge_id:
        raise ValueError("HUE_BRIDGE_ID not found")

    context = ssl.create_default_context(
        cafile=str(CA_BUNDLE)
    )

    context.check_hostname = True
    context.verify_mode = ssl.CERT_REQUIRED
    context.hostname_checks_common_name = True

    with socket.create_connection(
        (bridge_ip, 443),
        timeout=5,
    ) as sock:
        with context.wrap_socket(
            sock,
            server_hostname=bridge_id,
        ) as tls_socket:
            certificate = tls_socket.getpeercert()

            if certificate is None:
                raise RuntimeError(
                    "Hue Bridge did not provide a certificate."
                )

            print("\nTLS verification successful!")
            print("TLS version:", tls_socket.version())
            print("Cipher:", tls_socket.cipher())
            print("Subject:", certificate.get("subject"))
            print("Issuer:", certificate.get("issuer"))


if __name__ == "__main__":
    test_tls()