#!/usr/bin/env python3
"""
Breakout Room Allocator
Optimises group mixing across sessions for apprenticeship classes
"""

import os
import csv
import sys
import itertools
import random
from collections import defaultdict, Counter

SESSIONS = 8
LEARNER_CSV = 'data/groups.csv'

def load_learner_dict_from_csv(filename):
    print(filename)
    if not os.path.isfile(filename):
        # File not found, return default mapping: L1 -> L1, L2 -> L2, ..., L18 -> L18
        return {f'L{i}': f'L{i}' for i in range(1, 19)}
    
    learner_dict = {}
    try:
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                learner_dict[row['Code']] = row['Name']
        return learner_dict
    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return {f'L{i}': f'L{i}' for i in range(1, 19)}

# Load the learner names
learner_dict = load_learner_dict_from_csv(LEARNER_CSV)

def get_names_from_codes(code_list, learner_map):
    return [learner_map.get(code, f"Unknown({code})") for code in code_list]

def get_group_sizes(class_size):
    """Return the optimal group sizes for a given class size"""
    group_configs = {
         6: [3, 3],
         7: [3, 4], 
         8: [4, 4],
         9: [3, 3, 3],
        10: [3, 3, 4],
        11: [3, 4, 4],
        12: [4, 4, 4],  # [3, 3, 3, 3], 
        13: [3, 3, 3, 4],
        14: [3, 3, 4, 4],
        15: [3, 4, 4, 4],  # or [3, 3, 3, 3, 3],
        16: [4, 4, 4, 4],
        17: [3, 3, 3, 4, 4],
        18: [3, 3, 4, 4, 4],  # or [3, 3, 3, 3, 3, 3] 
    }
    return group_configs[class_size]    
    
class BreakoutAllocator:
    def __init__(self, class_size, sessions):
        self.class_size = class_size
        self.sessions = sessions
        self.learners = [f"L{i+1}" for i in range(class_size)]
        self.session_groups = []
        self.pair_sessions = defaultdict(list)  # Track which sessions each pair appears in
        self.learner_dict = learner_dict  # store name the mappings

    def create_valid_grouping(self, learner_list):
        groups = []
        group_sizes = get_group_sizes(len(learner_list))
        
        start = 0
        for size in group_sizes:
            groups.append(learner_list[start:start + size])
            start += size
        
        return groups
    
    def generate_all_possible_groupings(self):
        """Generate all possible ways to group learners"""
        groupings = []
        
        # Try multiple random arrangements and pick the best
        for _ in range(1000):
            shuffled = self.learners.copy()
            random.shuffle(shuffled)
            
            groups = self.create_valid_grouping(shuffled)
            
            # Only add valid groupings (all groups size 3-4)
            if groups and all(3 <= len(group) <= 4 for group in groups):
                groupings.append(groups)
        
        return groupings
    
    def get_all_pairs(self, group):
        """Get all pairs within a group"""
        return list(itertools.combinations(group, 2))
    
    def calculate_overlap_score(self, proposed_groups, session_num):
        """Calculate how many pair overlaps this grouping would create"""
        score = 0
        for group in proposed_groups:
            pairs = self.get_all_pairs(group)
            for pair in pairs:
                # Sort the pair to match storage format
                sorted_pair = tuple(sorted(pair))
                # Count how many times this pair has appeared before
                score += len(self.pair_sessions[sorted_pair])
        return score
    
    def update_pair_tracking(self, groups, session_num):
        """Update tracking of which pairs appear in which sessions"""
        for group in groups:
            pairs = self.get_all_pairs(group)
            for pair in pairs:
                # Ensure consistent ordering to avoid duplicates
                sorted_pair = tuple(sorted(pair))
                self.pair_sessions[sorted_pair].append(session_num)    

    def allocate_sessions(self):
        """Main allocation algorithm"""
        print(f"Allocating {self.class_size} learners into groups of 3-4 across {self.sessions} sessions...")
        
        for session in range(self.sessions):
            print(f"Planning session {session + 1}...")
            
            # Generate possible groupings
            possible_groupings = self.generate_all_possible_groupings()
            
            # Find the grouping with minimum overlap
            best_grouping = None
            best_score = float('inf')
            
            for grouping in possible_groupings:
                score = self.calculate_overlap_score(grouping, session)
                if score < best_score:
                    best_score = score
                    best_grouping = grouping
            
            # Safety check - if no valid grouping found, create a simple one
            if best_grouping is None:
                print(f"Warning: No optimal grouping found for session {session + 1}, using simple allocation")
                shuffled = self.learners.copy()
                random.shuffle(shuffled)
                best_grouping = self.create_valid_grouping(shuffled)
            
            # Use the best grouping for this session
            self.session_groups.append(best_grouping)
            self.update_pair_tracking(best_grouping, session + 1)

    def translate_group_codes_to_names(self, groups):
        """Convert groups of codes to groups of names"""
        return [[self.learner_dict.get(code, code) for code in group] for group in groups]

    def print_session_allocations(self):
        """Print the session allocations"""
        print(f"\n{'='*60}")
        print(f"BREAKOUT ROOM ALLOCATIONS - {self.class_size} LEARNERS")
        print(f"{'='*60}")
        
        for session_idx, groups in enumerate(self.session_groups):
            print(f"\nSESSION {session_idx + 1}:")
            named_groups = self.translate_group_codes_to_names(groups)
            for group_idx, group in enumerate(groups):
                learner_names = sorted([self.learner_dict.get(code, code) for code in group])
                print(f"  Group {group_idx + 1}: {', '.join(learner_names)}")
    
    def print_pair_matrix(self):
        """Print a matrix showing which sessions each pair worked together"""
        print(f"\n{'='*60}")
        print("PAIR COLLABORATION MATRIX")
        print("Numbers show which sessions learners worked together")
        print(f"{'='*60}")
        
        # Create header
        header = "    "
        for learner in self.learners:
            header += f"{learner:>6}"
        print(header)
        
        # Print matrix
        for i, learner1 in enumerate(self.learners):
            row = f"{learner1:>3} "
            for j, learner2 in enumerate(self.learners):
                if i == j:
                    row += "     -"
                elif i < j:
                    pair = tuple(sorted([learner1, learner2]))
                    sessions = self.pair_sessions.get(pair, [])
                    if sessions:
                        if len(sessions) <= 4:
                            session_str = ''.join(map(str, sessions))
                            row += f"{session_str:>6}"
                        else:
                            row += f"  {len(sessions)}x"
                    else:
                        row += "     ."
                else:
                    # Mirror the upper triangle
                    pair = tuple(sorted([learner2, learner1]))
                    sessions = self.pair_sessions.get(pair, [])
                    if sessions:
                        if len(sessions) <= 4:
                            session_str = ''.join(map(str, sessions))
                            row += f"{session_str:>6}"
                        else:
                            row += f"  {len(sessions)}x"
                    else:
                        row += "     ."
            print(row)
    
    def print_statistics(self):
        """Print allocation statistics"""
        print(f"\n{'='*60}")
        print("ALLOCATION STATISTICS")
        print(f"{'='*60}")

        # Count pair frequencies
        pair_counts = Counter()
        for pair, sessions in self.pair_sessions.items():
            pair_counts[len(sessions)] += 1

        total_possible_pairs = len(self.learners) * (len(self.learners) - 1) // 2
    
        # Calculate pairs that never worked together
        actual_pairs_worked = len([p for p in self.pair_sessions.values() if p])
        pair_counts[0] = total_possible_pairs - actual_pairs_worked

        print(f"Total possible pairs: {total_possible_pairs}")
        print(f"Pairs that never worked together: {pair_counts[0]} ({pair_counts[0]/total_possible_pairs*100:.1f}%)")
        
        for count in sorted(pair_counts.keys()):
            if count > 0:
                print(f"Pairs that worked together {count} time(s): {pair_counts[count]} ({pair_counts[count]/total_possible_pairs*100:.1f}%)")
        
        # Average meetings per person
        total_meetings = sum(len(sessions) for sessions in self.pair_sessions.values())
        meetings_per_person = (total_meetings * 2) / len(self.learners)  # *2 because each meeting involves 2 people
        print(f"\nAverage meetings per person: {meetings_per_person:.1f}")

def main(class_size, sessions):
    print("Breakout Room Allocator for Apprenticeship Classes")
    print("=" * 50)

    # Create allocator and run
    allocator = BreakoutAllocator(class_size, sessions)
    allocator.allocate_sessions()
    
    # Print results
    allocator.print_session_allocations()
    allocator.print_pair_matrix()
    allocator.print_statistics()
    
    print(f"\n{'='*60}")
    print(f"Allocation complete! Use these groups for your {sessions} breakout sessions.")
    print(f"{'='*60}")

if __name__ == "__main__":
    # Check if class size provided as argument
    if len(sys.argv) > 1:
        try:
            class_size = int(sys.argv[1])
            if not (6 <= class_size <= 18):
                print(f"Class size {class_size} not supported. Please use 6-18.")
                sys.exit()
            print(f"Using class size: {class_size}")
        except ValueError:
            print(f"Invalid class size: {sys.argv[1]}. Please use a number 6-18.")
            sys.exit()
    else:
        print("Please provide class size (6-18) as a command-line argument.")
        sys.exit(1)

    # Pass in sessions or use default 
    sessions = SESSIONS  # default
    if len(sys.argv) > 2:
        try:
            sessions = int(sys.argv[2])
            if sessions < 1 or sessions > SESSIONS:
                print(f"Number of sessions must be between 1 and {SESSIONS}.")
                sys.exit()
        except ValueError:
            print(f"Invalid number of sessions: {sys.argv[2]}. Please enter a positive integer.")
            sys.exit()

    main(class_size, sessions)
