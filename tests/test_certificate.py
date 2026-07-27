import os
import socket
import ssl

from dotenv import load_dotenv


load_dotenv()


def test_certificate():
    bridge_ip = os.getenv("HUE_BRIDGE_IP")
    bridge_id = os.getenv("HUE_BRIDGE_ID")

    if not bridge_ip:
        raise ValueError("HUE_BRIDGE_IP not found")

    if not bridge_id:
        raise ValueError("HUE_BRIDGE_ID not found")

    context = ssl._create_unverified_context()

    with socket.create_connection(
        (bridge_ip, 443),
        timeout=5,
    ) as sock:
        with context.wrap_socket(
            sock,
            server_hostname=bridge_id,
        ) as tls_socket:
            der_certificate = tls_socket.getpeercert(
                binary_form=True
            )

            if der_certificate is None:
                raise RuntimeError(
                    "Hue Bridge did not provide a certificate."
                )

            certificate = ssl.DER_cert_to_PEM_cert(
                der_certificate
            )

            print("\n--- HUE BRIDGE CERTIFICATE ---\n")
            print(certificate)
            print("TLS version:")
            print(tls_socket.version())
            print("\nCipher:")
            print(tls_socket.cipher())


if __name__ == "__main__":
    test_certificate()