
import asyncio
import os
import dotenv

import websockets
# noinspection PyPackageRequirements
import discord
# noinspection PyPackageRequirements
from discord import app_commands


dotenv.load_dotenv()


current_state = ""
connected = set()


async def handler(websocket: websockets.WebSocketServerProtocol):
    global current_state
    await websocket.send(current_state)
    connected.add(websocket)
    async for message in websocket:
        current_state = message
        await websocket.send(current_state)


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(websockets.serve(handler, '', 8001))

    intents = discord.Intents.default()
    client = discord.Client(intents=intents)
    command_tree = app_commands.CommandTree(client)

    @client.event
    async def on_ready():
        print(f'We have logged in as {client.user}')
        await command_tree.sync(guild=discord.Object(id=1119774583562711063))
        print("commands synced")

    @command_tree.command(
        name="statustext",
        description="update status text on stream",
        guild=discord.Object(id=1119774583562711063)
    )
    async def update_status_discord(interaction, new_status: str):
        global current_state
        current_state = new_status
        websockets.broadcast(connected, current_state)
        await interaction.response.send_message(f"published new status text to: `{new_status}`")


    client.run(os.environ.get("DISCORD_TOKEN"))
