import random
import concurrent.futures as futures


PROCESSES = 3
TOTAL = 100000


def main():
    exec_pool = futures.ProcessPoolExecutor(PROCESSES)
        
    # Choose the other door
    wins = play_games_in_parallel(
        process_pool = exec_pool, 
        number_of_processes = PROCESSES,
        number_of_games = TOTAL, 
        choose_other_door = True
    ) 
    ratio = float(wins) / float(TOTAL)
    print("When choosing the other door:")
    print(f"Win ratio: {wins}/{TOTAL} = {ratio}")

    # Keep the same door
    wins = play_games_in_parallel(
        process_pool = exec_pool, 
        number_of_processes = PROCESSES,
        number_of_games = TOTAL, 
        choose_other_door = False
    )   
    ratio = float(wins) / float(TOTAL)
    print("When keeping the same door:")
    print(f"Win ratio: {wins}/{TOTAL} = {ratio}")


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


def play_games(number_of_games, choose_other_door):
    wins = 0
    for i in range(0, number_of_games):
        wins += (play_game(choose_other_door) if 1 else 0)
    return wins


def play_games_in_parallel(process_pool, number_of_processes, number_of_games, choose_other_door):
    games_per_thread = int(number_of_games / number_of_processes)
    remainder_games = number_of_games % number_of_processes

    wins = 0
    tasks = []

    for i in range(0, number_of_processes):
        tasks.append(process_pool.submit(play_games, games_per_thread, choose_other_door))
    wins += play_games(remainder_games, choose_other_door)
    futures.wait(tasks)
    
    for task in tasks:
        wins += task.result()

    return wins


main()
