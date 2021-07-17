from state_and_action import State, Corner, Color, Edge, Action
from move import move

s = State({
    (1,1,1): Corner(Color.RED, Color.WHITE, Color.GREEN, Color.RED, Color.WHITE),
    (-1,1,1): Corner(Color.YELLOW, Color.RED, Color.GREEN, Color.YELLOW, Color.RED),
    (-1,-1,1): Corner(Color.RED, Color.BLUE, Color.YELLOW, Color.RED, Color.BLUE),
    (1,-1,1): Corner(Color.RED, Color.BLUE, Color.WHITE, Color.RED, Color.BLUE),
    (1,1,-1): Corner(Color.GREEN, Color.ORANGE, Color.WHITE, Color.GREEN, Color.ORANGE),
    (-1,1,-1): Corner(Color.GREEN, Color.ORANGE, Color.YELLOW, Color.GREEN, Color.ORANGE),
    (-1,-1,-1): Corner(Color.BLUE, Color.ORANGE, Color.YELLOW, Color.BLUE, Color.ORANGE),
    (1,-1,-1): Corner(Color.BLUE, Color.ORANGE, Color.WHITE, Color.BLUE, Color.ORANGE),
    (1,1,0): Edge(Color.WHITE, Color.GREEN, Color.WHITE, Color.GREEN),
    (-1,1,0): Edge(Color.GREEN, Color.YELLOW, Color.GREEN, Color.YELLOW),
    (-1,-1,0): Edge(Color.BLUE, Color.YELLOW, Color.BLUE, Color.YELLOW),
    (1,-1,0): Edge(Color.BLUE, Color.WHITE, Color.BLUE, Color.WHITE),
    (1,0,1): Edge(Color.RED, Color.WHITE, Color.RED, Color.WHITE),
    (-1,0,1): Edge(Color.RED, Color.YELLOW, Color.RED, Color.YELLOW),
    (-1,0,-1): Edge(Color.ORANGE, Color.YELLOW, Color.ORANGE, Color.YELLOW),
    (1,0,-1): Edge(Color.ORANGE, Color.WHITE, Color.ORANGE, Color.WHITE),
    (0,1,1): Edge(Color.RED, Color.GREEN, Color.RED, Color.GREEN),
    (0,-1,1): Edge(Color.RED, Color.BLUE, Color.RED, Color.BLUE),
    (0,-1,-1): Edge(Color.ORANGE, Color.BLUE, Color.ORANGE, Color.BLUE),
    (0,1,-1): Edge(Color.ORANGE, Color.GREEN, Color.ORANGE, Color.GREEN)
})

a = Action(Color.BLUE, False)
s = move(s, a)
s = move(s, a)
a = Action(Color.ORANGE, False)
s = move(s, a)
print(s)
