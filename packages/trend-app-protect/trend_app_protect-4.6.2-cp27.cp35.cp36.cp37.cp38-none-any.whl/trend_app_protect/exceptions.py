from __future__ import (
    absolute_import,
    division,
    print_function,
    unicode_literals,
)


class AgentError(RuntimeError):
    """
    Raised by the agent if run_hook failed and fail_closed=True.

    Meant to prevent situations where a request should have been blocked
    but wasn't because the agent wasn't ready yet, or there was an error
    in vmcode.
    """


class TrendAppProtectOverrideResponse(BaseException):
    """
    Raised by the agent to override the normal response for this request
    replace it with a new response instead.

    NOTE: We extend BaseException here to reduce the risk of being caught by
          a catch-all in customer code.
    """


class TrendAppProtectBlocked(Exception):
    """
    Raised by the agent in contexts where we cannot (or should not) override
    responses, e.g. in Lambda where there is no universal response format.

    This extends Exception so that it is handled by the Lambda Python runtime
    (BaseException is not caught and causes the runtime to not respond).
    """


class UnknownEngineError(Exception):
    """
    The Agent configuration has requested an unknown Engine class in
    its configuration.
    """


class ConfigError(Exception):
    """The Agent tried to load a configuration file but found an error."""
