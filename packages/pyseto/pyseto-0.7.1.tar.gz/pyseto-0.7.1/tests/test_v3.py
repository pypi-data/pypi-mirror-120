from secrets import token_bytes

import pytest

import pyseto
from pyseto import DecryptError, EncryptError, Key, VerifyError
from pyseto.versions.v3 import V3Local, V3Public

from .utils import load_key


class TestV3Local:
    """
    Tests for v3.local.
    """

    @pytest.mark.parametrize(
        "key, msg",
        [
            (b"", "key must be specified."),
        ],
    )
    def test_v3_local_new_with_invalid_arg(self, key, msg):
        with pytest.raises(ValueError) as err:
            Key.new("v3", "local", key)
            pytest.fail("Key.new() should fail.")
        assert msg in str(err.value)

    def test_v3_local_decrypt_via_decode_with_wrong_key(self):
        k1 = Key.new("v3", "local", b"our-secret")
        k2 = Key.new("v3", "local", b"others-secret")
        token = pyseto.encode(k1, b"Hello world!")
        with pytest.raises(DecryptError) as err:
            pyseto.decode(k2, token)
            pytest.fail("pyseto.decode() should fail.")
        assert "Failed to decrypt." in str(err.value)

    def test_v3_local_encrypt_with_invalid_arg(self):
        k = Key.new("v3", "local", b"our-secret")
        with pytest.raises(EncryptError) as err:
            k.encrypt(None)
            pytest.fail("pyseto.encrypt() should fail.")
        assert "Failed to encrypt." in str(err.value)

    @pytest.mark.parametrize(
        "nonce",
        [
            token_bytes(1),
            token_bytes(8),
            token_bytes(31),
            token_bytes(33),
            token_bytes(64),
        ],
    )
    def test_v3_local_encrypt_via_encode_with_wrong_nonce(self, nonce):
        k = Key.new("v3", "local", b"our-secret")
        with pytest.raises(ValueError) as err:
            pyseto.encode(k, b"Hello world!", nonce=nonce)
            pytest.fail("pyseto.encode() should fail.")
        assert "nonce must be 32 bytes long." in str(err.value)

    @pytest.mark.parametrize(
        "paserk, msg",
        [
            ("xx.local.AAAAAAAAAAAAAAAA", "Invalid PASERK version for a v3.local key."),
            ("k4.local.AAAAAAAAAAAAAAAA", "Invalid PASERK version for a v3.local key."),
            ("k3.xxx.AAAAAAAAAAAAAAAA", "Invalid PASERK type for a v3.local key."),
            ("k3.public.AAAAAAAAAAAAAAAA", "Invalid PASERK type for a v3.local key."),
        ],
    )
    def test_v3_local_from_paserk_with_invalid_args(self, paserk, msg):

        with pytest.raises(ValueError) as err:
            V3Local.from_paserk(paserk)
            pytest.fail("Key.from_paserk should fail.")
        assert msg in str(err.value)


class TestV3Public:
    """
    Tests for v3.public.
    """

    def test_v3_public_verify_via_encode_with_wrong_key(self):
        sk = Key.new("v3", "public", load_key("keys/private_key_ecdsa_p384.pem"))
        pk = Key.new("v3", "public", load_key("keys/public_key_ecdsa_p384_2.pem"))
        token = pyseto.encode(sk, b"Hello world!")
        with pytest.raises(VerifyError) as err:
            pyseto.decode(pk, token)
            pytest.fail("pyseto.decode() should fail.")
        assert "Failed to verify." in str(err.value)

    @pytest.mark.parametrize(
        "paserk, msg",
        [
            (
                "xx.public.AAAAAAAAAAAAAAAA",
                "Invalid PASERK version for a v3.public key.",
            ),
            (
                "k4.public.AAAAAAAAAAAAAAAA",
                "Invalid PASERK version for a v3.public key.",
            ),
            ("k3.xxx.AAAAAAAAAAAAAAAA", "Invalid PASERK type for a v3.public key."),
            ("k3.local.AAAAAAAAAAAAAAAA", "Invalid PASERK type for a v3.public key."),
        ],
    )
    def test_v3_public_from_paserk_with_invalid_args(self, paserk, msg):

        with pytest.raises(ValueError) as err:
            V3Public.from_paserk(paserk)
            pytest.fail("Key.from_paserk should fail.")
        assert msg in str(err.value)
