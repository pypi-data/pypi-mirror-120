# ******************************************************
# |docname| - Provide a scalable synchronous chat system
# ******************************************************
# For effective peer instructio in a mixed or online class we must support some
# kind of chat system.  This may spill over into other use cases but for now the
# peer instruction pages are the main use case.  To provide a near real time chat
# environment we need to use websockets.  This is a new area for us in summer 2021
# creating a websocket chat system is super simple for a toy environment. One server
# process can track all users and their connections, but in a production environment
# with multiple workers it gets much more complicated.  `this article <https://tsh.io/blog/how-to-scale-websocket/>`_
# does a nice job of explaining the issues and solutions.
#
# Our architecture is as follows:
# We will use redis pubsub model to support a fast production environment.
#
# We have one end point called ``websocket_endpoint`` that browsers open a websocket with
# this connection is only for the page to RECEIVE messages.  The endpoint is also a redis
# subscriber to the "peermessages" channel.
#
# We have a second endpoint called ``send_message`` that accepts a json formatted message
# package.  This could be a broadcast text message, or could be a special control mesage
# that allows the instructor to move the students through the peer process.  The ``send_message``
# endpoint is the redis producer.
#
# The producer sends the message into the redis queue and then all copies of the consumer
# look at the message.  If the recipient of that message is connected to that instance
# then the message is sent to the recipient and all other instance ignore that message.
# If the message is a broadcast message then all instances of the consumer forward that
# message to all connected parties.

import asyncio
import json

#
# Third-party imports
# -------------------
import os
from datetime import datetime
from typing import Dict, Optional

import aioredis
import async_timeout

# Local application imports
# -------------------------
from fastapi import (
    APIRouter,
    Cookie,
    Query,
    WebSocket,  # Depends,; noqa F401
    WebSocketDisconnect,
    status,
)
from fastapi.templating import Jinja2Templates

from ..applogger import rslogger
from ..config import settings
from ..crud import create_useinfo_entry
from ..models import UseinfoValidation
from ..schemas import PeerMessage

# from ..session import auth_manager

# Routing
# =======
# See `APIRouter config` for an explanation of this approach.
# Remove the "discuss" prefix until PR #2640 of FastAPI is merged
router = APIRouter(
    tags=["discuss"],
)

templates = Jinja2Templates(directory=f"{settings._book_server_path}/templates/discuss")


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}

    async def connect(self, user: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[user] = websocket

    def disconnect(self, sockid: str):
        del self.active_connections[sockid]

    async def send_personal_message(
        self,
        receiver: str,
        message: PeerMessage,
    ):
        to = receiver
        if to in self.active_connections:
            try:
                rslogger.debug(f"sending PM to {to} on {self.active_connections[to]}")
                await self.active_connections[to].send_json(message)
            except Exception as e:
                rslogger.error(f"Error sending to {to} is {e}")
                del self.active_connections[to]
        else:
            rslogger.error(f"{to} is not connected {self.active_connections}")

    async def broadcast(self, message: str):
        rslogger.debug(f"{self.active_connections=} {message=}")
        to_remove = []
        for key, connection in self.active_connections.items():
            rslogger.debug(f"sending to {connection}")
            res = None
            try:
                res = await connection.send_json(message)
            except Exception as e:
                rslogger.debug(f"Failed to send {e}")
                to_remove.append(key)
            rslogger.debug(f"result of send = {res}")
        for key in to_remove:
            del self.active_connections[key]


# this is good for prototyping, but we will need to integrate with
# Redis or a DB for production where we have multiple servers
manager = ConnectionManager()
local_users = set()


async def get_cookie_or_token(
    websocket: WebSocket,
    access_token: Optional[str] = Cookie(None),
    user: Optional[str] = Query(None),
):
    rslogger.debug(f"HELLO {access_token=} or {user=}")
    if access_token is None and user is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    return access_token or user


# It seems that ``@router.websocket`` is much better than the documented
# ``websocket_route``
@router.websocket("/chat/{uname}/ws")
async def websocket_endpoint(websocket: WebSocket, uname: str):
    """
    This endpoint is called to establish a websocket connection between
    The browser and the server.  The websocket is persistent as long
    as the process that runs this endpoint is alive.

    Note: This function must return which means it must be throroughly async
    Using a non async library like plain redis-py will not work as the subscriber
    will block
    """
    rslogger.debug(f"IN WEBSOCKET {uname=}")
    # res = await auth_manager.get_current_user(user)
    # username = res.username
    # rslogger.debug(f"{res=}")
    username = uname
    local_users.add(username)
    await manager.connect(username, websocket)
    r = aioredis.from_url(os.environ.get("REDIS_URI", "redis://localhost:6379/0"))
    subscriber = r.pubsub()
    await subscriber.subscribe("peermessages")
    # subscriber.subscribe(peermessages=callable) # in this case callable is automatically called
    try:
        while True:
            try:
                async with async_timeout.timeout(1):
                    pmess = await subscriber.get_message(ignore_subscribe_messages=True)
                    if pmess:
                        rslogger.debug(f"{pmess=}")
                        if pmess["type"] == "message":
                            # This is a message sent into the channel, our stuff is in
                            # the ``data`` field of the redis message
                            data = json.loads(pmess["data"])
                        else:
                            rslogger.error("unknown message type {pmess['type']}")
                            continue
                        if data["broadcast"]:
                            await manager.broadcast(data)
                        else:
                            # because **every** connection is in this loop we only
                            # want to send a non-broadcast message if it is to
                            # ourself.
                            partner = await r.hget("partnerdb", data["from"])
                            partner = partner.decode("utf8")
                            if partner == username:
                                await manager.send_personal_message(partner, data)
                                await create_useinfo_entry(
                                    UseinfoValidation(
                                        event="sendmessage",
                                        act=f"to:{partner}:{data['message']}",
                                        div_id=data["div_id"],
                                        course_id=data["course_name"],
                                        sid=username,
                                        timestamp=datetime.utcnow(),
                                    )
                                )
                            else:
                                rslogger.debug(f"{partner=} is not {username}")
            except asyncio.TimeoutError:
                pass

    except WebSocketDisconnect:
        manager.disconnect(username)
        rslogger.info(f"{username} has disconnected")


@router.post("/send_message")
async def send_message(packet: PeerMessage):
    r = await aioredis.from_url(os.environ.get("REDIS_URI", "redis://localhost:6379/0"))
    r.publish("peermessages", packet.json())
