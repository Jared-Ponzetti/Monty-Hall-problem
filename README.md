# Monty-Hall-problem

- The script uses the ProcessPoolExecutor from concurrent.futures to run the game simulations in parallel. (This was for fun, running 100 games is enough to show the two-thirds win chance of switching doors)
- The doors are represented as a set of three unique numbers. This allows for the set operators to be used to select subsets of the doors.
- Here is the code for simulating an individual game:
```python
def play_game(choose_other_door):

  # Possible doors are door 0, door 1, and door 2.
  doors = {0, 1, 2}

  # Choose a door to hide the car behind.
  car = {random.randint(0, 2)}
  goats = doors - car

  # Select one of the three doors at random.
  selected_door = {random.randint(0, 2)}

  # Reveal/remove a door that has a goat and is not selected.
  revealed_door = (goats - selected_door)
  if len(revealed_door) > 1:
      revealed_door.pop()

  # Choose to keep or change the selected door.
  if choose_other_door:
      selected_door = doors - revealed_door - selected_door
  else:
      selected_door = selected_door

  # Return boolean to indicate win or lose.
  return selected_door == car
```
