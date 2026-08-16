COMMAND_NAME = "ping"
COMMAND_DESC = "check how laggy poatochip is"

def get_ping_response(latency_ms: int) -> str:
    return f"poato chip pinged u after {latency_ms}ms?!"