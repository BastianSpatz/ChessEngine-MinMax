Chess in Python:
----
- Chessmain.py 	
- Engine.py 

Classes:
----
- Engine
	- Gamestate
		- This class stores all the information about the current gamestate. It will also determine 
			all the valid moves for the current state + MoveLog

How to implement game logic?
- Generate all possible moves for the player --> Generate all possible moves for the opposing player -->  
	Pawn movement + Capturing implemented.