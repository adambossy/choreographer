#!/usr/bin/python3
from enum import Enum, auto


# Source: https://salsahandbook.github.io/output/salsa-positions.html
# 2022/06/16Commenting out since these are not useful in isolation
#class HandPosition(Enum):
#    HalfClosed = auto(),
#    Open = auto(),
#    HalfOpenRightToLeft = auto(),
#    HalfOpenLeftToRight = auto(),
#    Handshake = auto(),
#    ReverseHandshake = auto(),
#    Crosshold = auto(),              # Leader's right over left
#    ReverseCrosshold = auto(),       # Leader's left over right
#    CrossedParallelHold = auto(), 
    

class PoseProperty(Enum):
    FacingEachOther = auto(),
    FacingOppositeDirection = auto(),
    FacingSameDirection = auto(),
    SideBySide = auto(),
    LeaderInFront = auto(),
    LeaderInBack = auto(),
    LeaderOnRight = auto(),
    LeaderOnLeft = auto(),
    RightToRight = auto(),
    LeftToLeft = auto(),
    LeftToRight = auto(),
    RightToLeft = auto(),
    LeadersRightOverLeadersLeft = auto(),
    LeadersLeftOverLeadersRight = auto(),
    LeadersRightHandOnFollowersBack = auto(),
    LeadersLeftHandOnFollowersBack = auto()


class Pose:

    def __init__(self, properties: [PoseProperty] = None):
        self.properties = properties or []

    def add_property(self, _property: PoseProperty):
        self.properties.append(_property)

    def __str__(self):
        return self.description


class Move:

    def __init__(self, start_pose, end_pose):
        self.start_pose = start_pose
        self.end_pose = end_pose


class Modifier:
    pass


class Routine:

    def __init__(self):
        self.moves = []

    def add(self, move: Move) -> None:
        self.moves.append(move)






## Salsa Positions
##
##  https://salsahandbook.github.io/output/salsa-positions.html





# Facing each other
# RightToLeft
# LeftToRight
# aka Parallel Handhold

open_position = Pose()
open_position.add_property(PoseProperty.FacingEachOther)
open_position.add_property(PoseProperty.RightToLeft)
open_position.add_property(PoseProperty.LeftToRight)

parallel_handhold = open_position # alias

closed_position = Pose()
closed_position.add_property(PoseProperty.FacingEachOther)
closed_position.add_property(PoseProperty.LeadersRightHandOnFollowersBack)

half_open_left_to_right = Pose()
half_open_left_to_right.add_property(PoseProperty.FacingEachOther)
half_open_left_to_right.add_property(PoseProperty.LeftToRight)


# Thought: should this be a different dataclass, like "Transition?"
scoop = Move(start_pose=open_position, end_pose=closed_position)

# There are tons of variations, e.g.,:
#   half closed position to half open left to right 
#   half closed position to open position
#   etc.. 
#
# Should I make different data types for each or can they be encapsulated in a single instance?
# Should this be a class that can have subclasses? Or somehow make all the variants connected? 
# How would a cross body lead with a leader's hook turn be called?
cross_body_lead = Move(start_pose=closed_position, end_pose=closed_position)

# Same issue here as with CBL. Can start in open_position or half_open_left_to_right and they effectively do the same thing...
follower_right_turn = Move(start_pose=open_position, end_pose=half_open_left_to_right)


follower_right_turn_to_cbl = Routine()
follower_right_turn_to_cbl.add(follower_right_turn)
follower_right_turn_to_cbl.add(scoop)
follower_right_turn_to_cbl.add(cross_body_lead)
