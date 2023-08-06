# =============================================================================== #
#                                                                                 #
#    This file has been generated automatically!! Do not change this manually!    #
#                                                                                 #
# =============================================================================== #
from __future__ import annotations

from pydantic import Field

from .message_sender import MessageSender
from ..base_object import BaseObject


class GroupCallRecentSpeaker(BaseObject):
    """
    Describes a recently speaking participant in a group call
    
    Params:
        participant_id (:class:`MessageSender`)
            Group call participant identifier
        
        is_speaking (:class:`bool`)
            True, is the user has spoken recently
        
    """

    ID: str = Field("groupCallRecentSpeaker", alias="@type")
    participant_id: MessageSender
    is_speaking: bool

    @staticmethod
    def read(q: dict) -> GroupCallRecentSpeaker:
        return GroupCallRecentSpeaker.construct(**q)
