import asyncio
import getpass
import json
import os
import websockets
from ai_agent.agent import *
import random

st = agent([1, 12.885008263218383, 15.842707182438396, 26.894496507795950, 27.6169140623970150, 30.185110719279040])
async def agent_loop(server_address="localhost:8000", agent_name="student"):
    async with websockets.connect(f"ws://{server_address}/player") as websocket:

        # Receive information about static game properties
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))
        prev = None
        while True:
            try:
                state = json.loads(
                    await websocket.recv()
                )  # receive game update, this must be called timely or your game will get out of sync with the server
                key = ""

                if "piece" in state.keys() and state["piece"]:
                    if prev == None or st.check == "error":
                        st.brain_cycle(state["game"],state["piece"],state["next_pieces"]) 
                    elif prev == state["game"] and not st.updating:
                        key = st.move_cycle(state["piece"])
                    else:
                        st.brain_cycle(state["game"],state["piece"],state["next_pieces"]) 
                     
                    prev = state["game"]

                await websocket.send(
                    json.dumps({"cmd": "key", "key": key})
                )  # send key command to server - you must implement this send in the AI agent
                
            except websockets.exceptions.ConnectionClosedOK:
                print("Server has cleanly disconnected us")
                return 
    



# DO NOT CHANGE THE LINES BELLOW
# You can change the default values using the command line, example:
# $ NAME='arrumador' python3 client.py
loop = asyncio.get_event_loop()
SERVER = os.environ.get("SERVER", "localhost")
PORT = os.environ.get("PORT", "8000")
NAME = os.environ.get("NAME", getpass.getuser())
loop.run_until_complete(agent_loop(f"{SERVER}:{PORT}", NAME))
