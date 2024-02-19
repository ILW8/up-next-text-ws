
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


async def handler(websocket: websockets.WebSocketServerProtocol):
    global current_state
    await websocket.send(current_state)
    async for message in websocket:
        current_state = message
        await websocket.send(current_state)


# async def ws_main():
#     # async with websockets.serve(handler, "", 8001):
#     #     await asyncio.Future()  # run forever
#     server = await websockets.serve(handler, '', 8001)
#     await server.wait_closed()


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
    async def first_command(interaction):
        await interaction.response.send_message("Hello!")


    client.run(os.environ.get("DISCORD_TOKEN"))
