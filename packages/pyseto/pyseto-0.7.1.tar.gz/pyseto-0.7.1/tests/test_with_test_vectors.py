import json

import pytest

import pyseto
from pyseto import Key
from pyseto.versions.v3 import V3Public

from .utils import get_path


def _load_tests(paths: list) -> list:
    tests: list = []
    for path in paths:
        with open(get_path(path)) as tv_file:
            tv = json.loads(tv_file.read())
        tests += tv["tests"]
    return tests


def _name_to_version(name: str) -> int:
    v = name.split(".")[0]
    if len(v) != 2:
        raise ValueError("Invalid PASERK test name.")
    return int(v[1:])


class TestWithTestVectors:
    """
    Tests with test vectors defined in https://github.com/paseto-standard/test-vectors.
    """

    @pytest.mark.parametrize(
        "v",
        _load_tests(
            [
                "vectors/v1.json",
                "vectors/v2.json",
                "vectors/v3.json",
                "vectors/v4.json",
            ]
        ),
    )
    def test_with_test_vectors(self, v):

        token = v["token"].encode("utf-8")
        payload = json.dumps(v["payload"], separators=(",", ":")).encode("utf-8")
        footer = v["footer"].encode("utf-8")
        implicit_assertion = v["implicit-assertion"].encode("utf-8")

        version = v["name"].split("-")[0]
        purpose = v["name"].split("-")[1]
        if purpose == "E":
            nonce = bytes.fromhex(v["nonce"])
            key = bytes.fromhex(v["key"])

            k = Key.new("v" + version, "local", key=key)
            encoded = pyseto.encode(k, payload, footer, implicit_assertion, nonce=nonce)
            decoded_token = pyseto.decode(k, token, implicit_assertion)
            decoded = pyseto.decode(k, encoded, implicit_assertion)
            assert payload == decoded_token.payload == decoded.payload
            return

        if purpose == "S":
            secret_key_pem = v["secret-key"] if version == "1" else v["secret-key-pem"]
            public_key_pem = v["public-key"] if version == "1" else v["public-key-pem"]

            sk = Key.new("v" + version, "public", secret_key_pem)
            encoded = pyseto.encode(sk, payload, footer, implicit_assertion)
            pk = Key.new("v" + version, "public", public_key_pem)
            decoded_token = pyseto.decode(pk, token, implicit_assertion)
            decoded = pyseto.decode(pk, encoded, implicit_assertion)
            assert payload == decoded_token.payload == decoded.payload

            if version == "1":
                return

            secret_key = bytes.fromhex(v["secret-key"])
            public_key = bytes.fromhex(v["public-key"])

            if version == "3":
                # TODO add support for secret-key/public-key on v3.public test vectors.
                return

            sk = Key.from_asymmetric_key_params("v" + version, d=secret_key[0:32])
            encoded = pyseto.encode(sk, payload, footer, implicit_assertion)
            pk = Key.from_asymmetric_key_params("v" + version, x=public_key)
            decoded_token = pyseto.decode(pk, token, implicit_assertion)
            decoded = pyseto.decode(pk, encoded, implicit_assertion)
            assert payload == decoded_token.payload == decoded.payload
            return
        pytest.fail(f"Invalid test name: {v['name']}")

    @pytest.mark.parametrize(
        "v",
        _load_tests(
            [
                "vectors/PASERK/k1.public.json",
                "vectors/PASERK/k2.public.json",
                "vectors/PASERK/k3.public.json",
                "vectors/PASERK/k4.public.json",
            ]
        ),
    )
    def test_with_test_vectors_paserk_public(self, v):

        version = _name_to_version(v["name"])
        if version == 1:
            k = Key.new(version, "public", v["key"])
        elif version == 2 or version == 4:
            k = Key.from_asymmetric_key_params(version, x=bytes.fromhex(v["key"]))
        elif version == 3:
            k = V3Public.from_public_bytes(bytes.fromhex(v["key"]))
        else:
            pytest.fail("Unsupported version.")
        assert k.to_paserk() == v["paserk"]
        k2 = Key.from_paserk(v["paserk"])
        assert k2.to_paserk() == v["paserk"]

    @pytest.mark.parametrize(
        "v",
        _load_tests(
            [
                "vectors/PASERK/k1.secret.json",
                "vectors/PASERK/k2.secret.json",
                # "vectors/PASERK/k3.secret.json",
                "vectors/PASERK/k4.secret.json",
            ]
        ),
    )
    def test_with_test_vectors_paserk_secret(self, v):

        version = _name_to_version(v["name"])
        if version == 1:
            k = Key.new(version, "public", v["key"])
        elif version == 2 or version == 4:
            k = Key.from_asymmetric_key_params(
                version, d=bytes.fromhex(v["secret-key-seed"])
            )
        elif version == 3:
            k = Key.new(version, "public", bytes.fromhex(v["key"]))
        else:
            pytest.fail("Unsupported version.")
        assert k.to_paserk() == v["paserk"]
        k2 = Key.from_paserk(v["paserk"])
        assert k2.to_paserk() == v["paserk"]

    @pytest.mark.parametrize(
        "v",
        _load_tests(
            [
                "vectors/PASERK/k1.local.json",
                "vectors/PASERK/k2.local.json",
                "vectors/PASERK/k3.local.json",
                "vectors/PASERK/k4.local.json",
            ]
        ),
    )
    def test_with_test_vectors_paserk_local(self, v):

        version = _name_to_version(v["name"])
        k = Key.new(version, "local", bytes.fromhex(v["key"]))
        k2 = Key.from_paserk(v["paserk"])
        assert k.to_paserk() == v["paserk"]
        assert k2.to_paserk() == v["paserk"]

    @pytest.mark.parametrize(
        "v",
        _load_tests(
            [
                "vectors/PASERK/k1.pid.json",
                "vectors/PASERK/k2.pid.json",
                "vectors/PASERK/k3.pid.json",
                "vectors/PASERK/k4.pid.json",
            ]
        ),
    )
    def test_with_test_vectors_paserk_pid(self, v):

        version = _name_to_version(v["name"])
        if version == 1:
            k = Key.new(version, "public", v["key"])
        elif version == 2 or version == 4:
            k = Key.from_asymmetric_key_params(version, x=bytes.fromhex(v["key"]))
        elif version == 3:
            k = V3Public.from_public_bytes(bytes.fromhex(v["key"]))
        else:
            pytest.fail("Unsupported version.")
        assert k.to_paserk_id() == v["paserk"]

    @pytest.mark.parametrize(
        "v",
        _load_tests(
            [
                "vectors/PASERK/k1.sid.json",
                "vectors/PASERK/k2.sid.json",
                # "vectors/PASERK/k3.sid.json",
                "vectors/PASERK/k4.sid.json",
            ]
        ),
    )
    def test_with_test_vectors_paserk_sid(self, v):

        version = _name_to_version(v["name"])
        if version == 1:
            k = Key.new(version, "public", v["key"])
        elif version == 2 or version == 4:
            k = Key.from_asymmetric_key_params(version, d=bytes.fromhex(v["seed"]))
        elif version == 3:
            k = Key.new(version, "public", bytes.fromhex(v["key"]))
        else:
            pytest.fail("Unsupported version.")
        assert k.to_paserk_id() == v["paserk"]

    @pytest.mark.parametrize(
        "v",
        _load_tests(
            [
                "vectors/PASERK/k1.lid.json",
                "vectors/PASERK/k2.lid.json",
                "vectors/PASERK/k3.lid.json",
                "vectors/PASERK/k4.lid.json",
            ]
        ),
    )
    def test_with_test_vectors_paserk_lid(self, v):

        version = _name_to_version(v["name"])
        k = Key.new(version, "local", bytes.fromhex(v["key"]))
        assert k.to_paserk_id() == v["paserk"]
