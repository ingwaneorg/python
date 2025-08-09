import random
import sys

def pick_and_remove(source, target):
    i = random.randrange(len(source))
    target.append(source.pop(i))

def move_random_numbers(source, count):
    target = []
    for _ in range(min(count, len(source))):
        pick_and_remove(source, target)
    return target

def get_numbers(target, count):

    numbers = list(range(1, target+1))
    selected = move_random_numbers(numbers, count)
    selected_sorted = sorted(selected) 

    return selected_sorted

def main():
    print()

    #  Lotto
    picks = get_numbers(59, 6)
    print(f"NL: {picks}\n")
    
    # Set for Life
    picks = get_numbers(47, 5)
    bonus = get_numbers(10, 1)
    print(f"SL: {picks} - {bonus}\n")
    
    # Euromillions
    picks = get_numbers(50, 5)
    bonus = get_numbers(12, 2)
    print(f"EM: {picks} - {bonus}\n")
    
    # Thunderball
    picks = get_numbers(39, 5)
    bonus = get_numbers(14, 1)
    print(f"TB: {picks} - {bonus}\n")
    


if __name__ == "__main__":
    main()

