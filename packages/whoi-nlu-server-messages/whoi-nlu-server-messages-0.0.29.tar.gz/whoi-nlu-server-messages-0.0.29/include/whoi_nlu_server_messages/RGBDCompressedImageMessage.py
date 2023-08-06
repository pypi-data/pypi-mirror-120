import dataclasses

from whoi_nlu_server_messages.CBorMessage import CBorMessage
from whoi_nlu_server_messages.HeaderMessage import HeaderMessage


@dataclasses.dataclass
class RGBDCompressedImageMessage(CBorMessage):
    header: HeaderMessage
    format: str
    data: bytearray
    # same params as above but for depth data
    d_format: str
    d_data: bytearray
    # Projection/camera matrix
    #     [fx'  0  cx' Tx]
    # P = [ 0  fy' cy' Ty]
    #     [ 0   0   1   0]
    P: list
