from dotenv import load_dotenv

load_dotenv()

from livekit.agents import (
    Agent,
    AgentServer,
    AgentSession,
    JobContext,
    cli,
)

from livekit.plugins.deepgram import STT, TTS


server = AgentServer()


@server.rtc_session()
async def entrypoint(ctx: JobContext):

    print("ENTRYPOINT STARTED")

    await ctx.connect()

    print("CONNECTED TO ROOM")

    participant = await ctx.wait_for_participant()

    print(f"PARTICIPANT JOINED: {participant.identity}")

    agent = Agent(
        instructions="""
You are a professional AI interviewer.

Be friendly and professional.

Speak naturally.

Wait for the candidate to finish speaking.

Do not interrupt the candidate.

Keep your responses concise.
"""
    )

    session = AgentSession(
        stt=STT(
            model="nova-3",
            language="en-IN",
        ),
        tts=TTS(
            model="aura-asteria-en",
        ),
    )

    await session.start(
        agent=agent,
        room=ctx.room,
    )

    print("SESSION STARTED")

    await session.say(
        "Welcome to the AI Interview. Please tell me your name."
    )

    print("WELCOME SENT")


if __name__ == "__main__":
    cli.run_app(server)
