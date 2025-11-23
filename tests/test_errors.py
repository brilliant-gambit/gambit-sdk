from gambit_sdk.errors.gambit_sdk_errors import (
    GambitSDKError,
    PlatformAuthenticationError,
    RefreshNotSupportedError,
)


def test_gambit_sdk_error_init() -> None:
    msg = "Base error"
    err = GambitSDKError(message=msg)
    assert str(err) == msg
    assert err.message == msg


def test_platform_authentication_error_init() -> None:
    msg = "Auth failed"
    err = PlatformAuthenticationError(message=msg)
    assert str(err) == msg
    assert isinstance(err, GambitSDKError)


def test_refresh_not_supported_error_init() -> None:
    msg = "Refresh not supported"
    err = RefreshNotSupportedError(message=msg)
    assert str(err) == msg
    assert isinstance(err, GambitSDKError)
