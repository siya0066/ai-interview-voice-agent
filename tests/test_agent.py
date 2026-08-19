from livekit.agents import AgentServer


def test_agent_server_exists():
    from agent import server

    assert isinstance(server, AgentServer)
