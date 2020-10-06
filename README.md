# Chess
Here's a chess engine project I developed during the lockdown. There's essentially 3 components here :

1- A **brute-force** chess engine. Given a parameter k. It makes a DFS of all possibilities the next k moves, attributes a score to each scenario and picks the best one. (Assuming the opponent does what's best for him too.)

**Result:** I am an amateur (more than a beginner) and I lost to it about 90% of the time for k=3. But for k>3 it starts to be very slow over my personal (cheap) PC.

2- A trained **machine-learning** model over 100K moves during games in professional tournaments. 
There's 7 submodels, one to decide which type of piece to move, the other 6 to decide the destination given the type of piece.

**Result:** It has an accuracy of about 30%. This is very good considering the fact that in the remaining 70% of the time, it may make a very good move that happens not to be the one the player made at the situation.
However, when confronted to an amateur like me, it seems very confused. Maybe I should have a more homogeneous dataset...


3- A **user interface**. By the end of the lockdown I had started designing a prettier interface but never had the time to finish it, so I figured I'll leave this one for demo purposes.

**Result:** Ugly, very ugly.
