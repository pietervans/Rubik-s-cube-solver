from state_and_action import State, Action
from copy import deepcopy


def move(state: State, action: Action) -> State:
    positions = deepcopy(state.positions)
    new_positions = dict()
    colorDict = action.getColorDict()
    dataNewPosition = action.getDataNewPosition()
    coord_ind, val = action.getFaceCoordinateValue()
    for pos, elem in positions.items():
        if pos[coord_ind] == val:
            if elem.orientation != action.face:
                elem.orientation = colorDict[elem.orientation]
            # change orientation of elem
            if elem.orientation2 != action.face:
                elem.orientation2 = colorDict[elem.orientation2]
            # add to new_positions at right position
            new_pos = action.getNewPosition(pos, *dataNewPosition)
            new_positions[new_pos] = elem
    positions.update(new_positions)
    return State(positions)
