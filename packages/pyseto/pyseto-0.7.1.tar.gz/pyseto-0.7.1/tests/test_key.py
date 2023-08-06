from secrets import token_bytes

import pytest

from pyseto import Key, NotSupportedError
from pyseto.key_interface import KeyInterface
from pyseto.utils import base64url_decode

from .utils import load_jwk, load_key


class TestKey:
    """
    Tests for Key.
    """

    @pytest.mark.parametrize(
        "version, type, key",
        [
            (1, "local", token_bytes(32)),
            (2, "local", token_bytes(32)),
            (3, "local", token_bytes(32)),
            (4, "local", token_bytes(32)),
        ],
    )
    def test_key_new_local(self, version, type, key):
        k = Key.new(version, type, key)
        assert isinstance(k, KeyInterface)
        assert k.version == version
        assert k.type == type
        with pytest.raises(NotSupportedError) as err:
            k.sign(b"Hello world!")
            pytest.fail("Key.sign() should fail.")
        assert "A key for local does not have sign()." in str(err.value)
        with pytest.raises(NotSupportedError) as err:
            k.verify(b"xxxxxx")
            pytest.fail("Key.verify() should fail.")
        assert "A key for local does not have verify()." in str(err.value)

    @pytest.mark.parametrize(
        "version, type, key",
        [
            (1, "public", load_key("keys/private_key_rsa.pem")),
            (1, "public", load_key("keys/public_key_rsa.pem")),
            (2, "public", load_key("keys/private_key_ed25519.pem")),
            (2, "public", load_key("keys/public_key_ed25519.pem")),
            (3, "public", load_key("keys/private_key_ecdsa_p384.pem")),
            (3, "public", load_key("keys/public_key_ecdsa_p384.pem")),
            (4, "public", load_key("keys/private_key_ed25519.pem")),
            (4, "public", load_key("keys/public_key_ed25519.pem")),
        ],
    )
    def test_key_new_public(self, version, type, key):
        k = Key.new(version, type, key)
        assert isinstance(k, KeyInterface)
        assert k.version == version
        assert k.type == type
        with pytest.raises(NotSupportedError) as err:
            k.encrypt(b"Hello world!")
            pytest.fail("Key.sign() should fail.")
        assert "A key for public does not have encrypt()." in str(err.value)
        with pytest.raises(NotSupportedError) as err:
            k.decrypt(b"xxxxxx")
            pytest.fail("Key.verify() should fail.")
        assert "A key for public does not have decrypt()." in str(err.value)

    @pytest.mark.parametrize(
        "version, key, msg",
        [
            ("v1", load_key("keys/private_key_ed25519.pem"), "The key is not RSA key."),
            ("v1", load_key("keys/public_key_ed25519.pem"), "The key is not RSA key."),
            (
                "v1",
                load_key("keys/private_key_ecdsa_p384.pem"),
                "The key is not RSA key.",
            ),
            (
                "v1",
                load_key("keys/public_key_ecdsa_p384.pem"),
                "The key is not RSA key.",
            ),
            ("v2", load_key("keys/private_key_rsa.pem"), "The key is not Ed25519 key."),
            ("v2", load_key("keys/public_key_rsa.pem"), "The key is not Ed25519 key."),
            (
                "v2",
                load_key("keys/private_key_ecdsa_p384.pem"),
                "The key is not Ed25519 key.",
            ),
            (
                "v2",
                load_key("keys/public_key_ecdsa_p384.pem"),
                "The key is not Ed25519 key.",
            ),
            (
                "v3",
                load_key("keys/private_key_ed25519.pem"),
                "The key is not ECDSA key.",
            ),
            (
                "v3",
                load_key("keys/public_key_ed25519.pem"),
                "The key is not ECDSA key.",
            ),
            ("v3", load_key("keys/private_key_rsa.pem"), "The key is not ECDSA key."),
            ("v3", load_key("keys/public_key_rsa.pem"), "The key is not ECDSA key."),
            ("v4", load_key("keys/private_key_rsa.pem"), "The key is not Ed25519 key."),
            ("v4", load_key("keys/public_key_rsa.pem"), "The key is not Ed25519 key."),
            (
                "v4",
                load_key("keys/private_key_ecdsa_p384.pem"),
                "The key is not Ed25519 key.",
            ),
            (
                "v4",
                load_key("keys/public_key_ecdsa_p384.pem"),
                "The key is not Ed25519 key.",
            ),
        ],
    )
    def test_key_new_public_with_wrong_key(self, version, key, msg):
        with pytest.raises(ValueError) as err:
            Key.new(version, "public", key)
            pytest.fail("Key.new should fail.")
        assert msg in str(err.value)

    @pytest.mark.parametrize(
        "version, type, key, msg",
        [
            ("v*", "local", token_bytes(32), "Invalid version: v*."),
            ("v0", "local", token_bytes(32), "Invalid version: v0."),
            (0, "local", token_bytes(32), "Invalid version: 0."),
            (
                "v*",
                "public",
                load_key("keys/private_key_rsa.pem"),
                "Invalid version: v*.",
            ),
            (
                "v0",
                "public",
                load_key("keys/private_key_rsa.pem"),
                "Invalid version: v0.",
            ),
            (
                0,
                "public",
                load_key("keys/private_key_rsa.pem"),
                "Invalid version: 0.",
            ),
            ("v1", "xxx", token_bytes(32), "Invalid type(purpose): xxx."),
            ("v1", "public", "-----BEGIN BAD", "Invalid or unsupported PEM format."),
        ],
    )
    def test_key_new_with_invalid_arg(self, version, type, key, msg):
        with pytest.raises(ValueError) as err:
            Key.new(version, type, key)
            pytest.fail("Key.new should fail.")
        assert msg in str(err.value)

    @pytest.mark.parametrize(
        "version, key",
        [
            # (1, load_jwk("keys/private_key_rsa.json")),
            # (1, load_jwk("keys/public_key_rsa.json")),
            (2, load_jwk("keys/private_key_ed25519.json")),
            (2, load_jwk("keys/public_key_ed25519.json")),
            (3, load_jwk("keys/private_key_ecdsa_p384.json")),
            (3, load_jwk("keys/public_key_ecdsa_p384.json")),
            (4, load_jwk("keys/private_key_ed25519.json")),
            (4, load_jwk("keys/public_key_ed25519.json")),
        ],
    )
    def test_key_from_asymmetric_params(self, version, key):

        k = Key.from_asymmetric_key_params(version, x=key["x"], y=key["y"], d=key["d"])
        assert isinstance(k, KeyInterface)
        assert k.version == version
        assert k.type == "public"

    @pytest.mark.parametrize(
        "paserk, msg",
        [
            ("v1.local.AAAAAAAAAAAAAAAA", "Invalid PASERK version: v1."),
            ("*.local.AAAAAAAAAAAAAAAA", "Invalid PASERK version: *."),
            ("k1.xxx.AAAAAAAAAAAAAAAA", "Invalid PASERK key type: xxx."),
        ],
    )
    def test_key_from_paserk_with_invalid_args(self, paserk, msg):

        with pytest.raises(ValueError) as err:
            Key.from_paserk(paserk)
            pytest.fail("Key.from_paserk should fail.")
        assert msg in str(err.value)

    @pytest.mark.parametrize(
        "version, key, msg",
        [
            (
                "v1",
                load_jwk("keys/private_key_rsa.json"),
                "v1.public is not supported on from_key_parameters.",
            ),
            ("v*", load_jwk("keys/private_key_ed25519.json"), "Invalid version: v*."),
            (0, load_jwk("keys/private_key_ed25519.json"), "Invalid version: 0."),
            (
                "v2",
                {"x": b"xxx", "y": b"", "d": b"ddd"},
                "Only one of x or d should be set for v2.public.",
            ),
            ("v2", {"x": b"xxx", "y": b"", "d": b""}, "Failed to load key."),
            ("v2", {"x": b"", "y": b"", "d": b"ddd"}, "Failed to load key."),
            (
                "v2",
                {"x": b"", "y": b"", "d": b""},
                "x or d should be set for v2.public.",
            ),
            (
                "v3",
                {"x": b"xxx", "y": b"", "d": b"ddd"},
                "x and y (and d) should be set for v3.public.",
            ),
            (
                "v3",
                {"x": b"", "y": b"yyy", "d": b"ddd"},
                "x and y (and d) should be set for v3.public.",
            ),
            ("v3", {"x": b"xxx", "y": b"yyy", "d": b""}, "Failed to load key."),
            (
                "v3",
                {
                    "x": base64url_decode(
                        "_XyN9woHaS0mPimSW-etwJMEDSzxIMjp4PjezavU8SHJoClz1bQrcmPb1ZJxHxhI"
                    ),
                    "y": base64url_decode(
                        "GCNfc32p9sRotx7u2oDGJ3Eqz6q5zPHLdizNn83oRsUTN31eCWfGLHWRury3xF50"
                    ),
                    "d": b"ddd",
                },
                "Failed to load key.",
            ),
            (
                "v4",
                {"x": b"xxx", "y": b"", "d": b"ddd"},
                "Only one of x or d should be set for v4.public.",
            ),
            ("v4", {"x": b"xxx", "y": b"", "d": b""}, "Failed to load key."),
            ("v4", {"x": b"", "y": b"", "d": b"ddd"}, "Failed to load key."),
            (
                "v4",
                {"x": b"", "y": b"", "d": b""},
                "x or d should be set for v4.public.",
            ),
        ],
    )
    def test_key_from_asymmetric_params_with_invalid_arg(self, version, key, msg):

        with pytest.raises(ValueError) as err:
            Key.from_asymmetric_key_params(version, x=key["x"], y=key["y"], d=key["d"])
            pytest.fail("Key.from_asymmetric_key_params() should fail.")
        assert msg in str(err.value)

    @pytest.mark.parametrize(
        "version, type, key",
        [
            (1, "public", load_key("keys/public_key_rsa.pem")),
            (2, "public", load_key("keys/public_key_ed25519.pem")),
            (3, "public", load_key("keys/public_key_ecdsa_p384.pem")),
            (4, "public", load_key("keys/public_key_ed25519.pem")),
        ],
    )
    def test_key_to_paserk_public(self, version, type, key):
        k = Key.new(version, type, key)
        assert k.to_paserk().startswith(f"k{k.version}.public.")

    @pytest.mark.parametrize(
        "version, type, key",
        [
            (1, "public", load_key("keys/private_key_rsa.pem")),
            (2, "public", load_key("keys/private_key_ed25519.pem")),
            (3, "public", load_key("keys/private_key_ecdsa_p384.pem")),
            (4, "public", load_key("keys/private_key_ed25519.pem")),
        ],
    )
    def test_key_to_paserk_secret(self, version, type, key):
        k = Key.new(version, type, key)
        assert k.to_paserk().startswith(f"k{k.version}.secret.")
