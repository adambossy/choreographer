#!/usr/bin/python3
from collections import defaultdict
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

    def __init__(self, name: str, properties: [PoseProperty] = None):
        self.name = name
        self.properties = properties or []

    def add_property(self, _property: PoseProperty):
        self.properties.append(_property)

    def __repr__(self) -> str:
        return self.name # + '\n'.join(map(str, self.properties))


class Move:

    def __init__(self, name: str, pose_pairings=[(Pose, Pose)]):
        self.name = name
        self.pose_pairings = pose_pairings

    def __repr__(self):
        return self.name


class Modifier:
    pass


class Routine:

    def __init__(self):
        self.moves = []

    def add(self, move: Move) -> None:
        self.moves.append(move)


class MoveIndex:

    def __init__(self, moves):
        self.moves = moves
        self._build_index()

    def _build_index(self) -> None:
        self.index = defaultdict(set)
        for move in self.moves:
            for start_pose, end_pose in move.pose_pairings:
                self.index[start_pose].add(move)

    def next(self, end_pose: Pose) -> [Move]:
        return self.index[end_pose]


## Salsa Positions
##
##  https://salsahandbook.github.io/output/salsa-positions.html


# Facing each other
# RightToLeft
# LeftToRight
# aka Parallel Handhold

open_position = Pose(name="Open Position")
open_position.add_property(PoseProperty.FacingEachOther)
open_position.add_property(PoseProperty.RightToLeft)
open_position.add_property(PoseProperty.LeftToRight)

parallel_handhold = open_position # alias

closed_position = Pose(name="Closed Position")
closed_position.add_property(PoseProperty.FacingEachOther)
closed_position.add_property(PoseProperty.LeadersRightHandOnFollowersBack)
closed_position.add_property(PoseProperty.LeftToRight)

half_closed_position = Pose(name="Half Closed Position")
half_closed_position.add_property(PoseProperty.FacingEachOther)
half_closed_position.add_property(PoseProperty.LeadersRightHandOnFollowersBack)

half_open_left_to_right = Pose(name="Half Open Left To Right")
half_open_left_to_right.add_property(PoseProperty.FacingEachOther)
half_open_left_to_right.add_property(PoseProperty.LeftToRight)

half_open_right_to_left = Pose(name="Half Open Right To Left")
half_open_right_to_left.add_property(PoseProperty.FacingEachOther)
half_open_right_to_left.add_property(PoseProperty.RightToLeft)

hammerlock = Pose("Hammerlock")
half_open_right_to_left.add_property(PoseProperty.RightToLeft)
half_open_right_to_left.add_property(PoseProperty.LeftToRight)

handshake = Pose("handshake")
handshake.add_property(PoseProperty.RightToRight)

# Thought: should this be a different dataclass, like "Transition?"
scoop = Move(
    name="Scoop",
    pose_pairings=[
        (half_open_left_to_right, closed_position)
    ]
)

# There are tons of variations, e.g.,:
#   half closed position to half open left to right 
#   half closed position to open position
#   etc.. 
#
# Should I make different data types for each or can they be encapsulated in a single instance?
# Should this be a class that can have subclasses? Or somehow make all the variants connected? 
# How would a cross body lead with a leader's hook turn be called?
cross_body_lead = Move(
    name="Cross Body Lead",
    pose_pairings=[
        (closed_position, closed_position),
        (closed_position, open_position),
        (closed_position, half_open_left_to_right),
        (half_closed_position, closed_position),
        (half_closed_position, open_position),
        (half_closed_position, half_open_left_to_right),
        (open_position, open_position),
        (open_position, half_open_left_to_right),
    ]
)

# Youtube: https://www.youtube.com/watch?v=kFTB6-gOgII&list=PLzGRdLHrtfBxrumg9IrbyqP2KZfeV1wYi&index=7
reverse_cross_body_lead = Move(
    name="Reverse Cross Body Lead",
    pose_pairings=[
        (closed_position, closed_position)
    ]
)

# Youtube: https://www.youtube.com/watch?v=k3b5gh1V_Ts
back_spot_turn = Move(
    name="Back Spot Turn",
    pose_pairings=[
        (half_open_left_to_right, closed_position),
        (half_open_left_to_right, half_closed_position),
        (closed_position, closed_position),
        (closed_position, half_closed_position),
    ]
)

lead_right_turn = Move(
    name="Lead Right Turn",
    pose_pairings=[
        (half_open_left_to_right, half_open_left_to_right),
        # TODO add more pairings
    ]
)

# Same issue here as with CBL. Can start in open_position or half_open_left_to_right and they effectively do the same thing...
follower_right_turn = Move(
    name="Follower Right Turn",
    pose_pairings=[
        (open_position, open_position),
        (open_position, half_open_left_to_right),
        (open_position, half_open_right_to_left),
        (half_open_left_to_right, half_open_left_to_right),
        (half_open_right_to_left, half_open_right_to_left)
    ]
)

lead_left_turn = Move(
    name="Lead Left Turn",
    pose_pairings=[
        (half_open_left_to_right, half_open_left_to_right),
        # TODO add more pairings
    ]
)

follower_left_turn = Move(
    name="Follower Left Turn",
    pose_pairings=[
        (open_position, half_open_left_to_right),
    ]
)

lead_hook_turn = Move(
    name="Lead Hook Turn",
    pose_pairings=[
        (half_open_left_to_right, handshake),
        # TODO add more pairings
    ]
)

new_york_walk = Move(
    name="New York Walk",
    pose_pairings=[
        (half_open_left_to_right, half_open_left_to_right)
    ]
)

inside_turn = Move(
    name="Inside Turn",
    pose_pairings=[
        (closed_position, closed_position),
        (closed_position, half_open_left_to_right)
    ]
)

reverse_inside_turn = Move(
    name="Reverse Inside Turn",
    pose_pairings=[
        (half_open_left_to_right, half_open_left_to_right),
    ]
)

# Youtube: https://www.youtube.com/watch?v=IILWDseswo4&list=PLzGRdLHrtfBxrumg9IrbyqP2KZfeV1wYi&index=6
outside_turn = Move(
    name="Outside Turn",
    pose_pairings=[
        (half_open_left_to_right, half_open_left_to_right)
    ]
)

# Youtube: https://www.youtube.com/watch?v=W-CX-HVW43o&list=PLzGRdLHrtfBxrumg9IrbyqP2KZfeV1wYi&index=8
the_hesitation = Move(
    name="The Hesitation",
    pose_pairings=[
        (closed_position, closed_position)
    ]
)

# Youtube: https://www.youtube.com/watch?v=Yuwjs0Rgc7g&list=PLzGRdLHrtfBxrumg9IrbyqP2KZfeV1wYi&index=9
# Thought: this is CBL + leaders left turn. Maybe make a "prereqs" field? It really is its own move...
suave = Move(
    name="Suave",
    pose_pairings=[
        (half_open_left_to_right, half_open_left_to_right),
    ]
)

# Youtube: https://www.youtube.com/watch?v=xV0dk0IA8MM&list=PLzGRdLHrtfBxrumg9IrbyqP2KZfeV1wYi&index=10
# CBL + leaders hook turn
rejection = Move(
    name="Rejection",
    pose_pairings=[
        (open_position, open_position),
        (open_position, half_open_left_to_right),
        (half_open_left_to_right, half_open_left_to_right),
        (half_open_left_to_right, open_position)
    ]
)


follower_right_turn_to_cbl = Routine()
follower_right_turn_to_cbl.add(follower_right_turn)
follower_right_turn_to_cbl.add(scoop)
follower_right_turn_to_cbl.add(cross_body_lead)


move_index = MoveIndex([
    scoop,
    cross_body_lead,
    reverse_cross_body_lead,
    back_spot_turn,
    follower_right_turn,
    follower_left_turn,
    new_york_walk,
    inside_turn,
    reverse_inside_turn,
    outside_turn,
    the_hesitation,
    suave,
    rejection,
])

print("What can I do from open position?")
print('\n'.join(map(str, move_index.next(open_position))))
print('\n')


print("What can I do from closed position?")
print('\n'.join(map(str, move_index.next(closed_position))))
print('\n')


print("What can I do from half open left to right?")
print('\n'.join(map(str, move_index.next(half_open_left_to_right))))
print('\n')


# Youtube: https://www.youtube.com/watch?v=DrWfGWTu8DI&list=PLzGRdLHrtfBznMVEaqCVr90dwu08fKu7t&index=2
challenge_routine = Routine()
challenge_routine.add(follower_right_turn) # Right To Left handhold
# challenge_routine.add(hair_comb_with_left_to_right_pickup)
challenge_routine.add(outside_turn) # Left To Right handhold
challenge_routine.add(follower_right_turn) # Left To Right with release and pickup
challenge_routine.add(cross_body_lead) # With pickup to closed position
challenge_routine.add(cross_body_lead) # With transition to open position


# Nieves Salsa Class 2022/06/20
nieves_2022_06_20_routine = Routine()
nieves_2022_06_20_routine.add(cross_body_lead)
## TODO: add open break variation
nieves_2022_06_20_routine.add(back_spot_turn)
## TODO: add modifier to indicate the lead doesn't fully close, but transitions through
nieves_2022_06_20_routine.add(cross_body_lead) 
## TODO: add modifier that the lead transitions from half-closed to half-open left to right
nieves_2022_06_20_routine.add(follower_right_turn)
nieves_2022_06_20_routine.add(reverse_inside_turn)
nieves_2022_06_20_routine.add(lead_left_turn)
# The next part could be a separate routine!
nieves_2022_06_20_routine.add(follower_right_turn)
nieves_2022_06_20_routine.add(lead_right_turn)
nieves_2022_06_20_routine.add(lead_hook_turn)
# TODO add follower's booty roll


# TODO add jun 17 salsa salsa class (enchuflas!)

