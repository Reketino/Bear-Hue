import ssl

import urllib3


class HueHTTPS:
    def __init__(
        self,
        bridge_ip: str,
        bridge_id: str,
        ca_bundle: str,
    ) -> None:
        self.bridge_ip = bridge_ip
        self.bridge_id = bridge_id.lower()

        ssl_context = ssl.create_default_context(
            cafile=ca_bundle
        )

        ssl_context.verify_mode = ssl.CERT_REQUIRED
        ssl_context.check_hostname = True
        ssl_context.hostname_checks_common_name = True

        self.pool = urllib3.HTTPSConnectionPool(
            host=self.bridge_ip,
            port=443,
            ssl_context=ssl_context,
            assert_hostname=self.bridge_id,
            server_hostname=self.bridge_id,
            maxsize=4,
        )

    def get(
        self,
        endpoint: str,
        headers: dict[str, str] | None = None,
    ):
        response = self.pool.request(
            "GET",
            endpoint,
            headers=headers,
            timeout=5.0,
        )

        if response.status >= 400:
            raise RuntimeError(f"Hue HTTPS GET failed with status {response.status}")

        return response.json()

    def put(
        self,
        endpoint: str,
        payload: dict,
        headers: dict[str, str] | None = None,
    ):
        response = self.pool.request(
            "PUT",
            endpoint,
            headers=headers,
            json=payload,
            timeout=5.0,
        )

        if response.status >= 400:
            raise RuntimeError(f"Hue HTTPS PUT failed with status {response.status}")

        return response.json()