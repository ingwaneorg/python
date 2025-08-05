#!/usr/bin/env python3
"""
Breakout Room Allocator
Optimises group mixing across sessions for apprenticeship classes
"""

import os
import csv
import itertools
import random
import click
from collections import defaultdict, Counter
from pathlib import Path

def load_learner_dict_from_csv(filename):
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
        click.echo(f"Error reading {filename}: {e}")
        return {f'L{i}': f'L{i}' for i in range(1, 19)}

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
    def __init__(self, class_size, sessions, learner_dict):
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
        click.echo(f"Allocating {self.class_size} learners into groups of 3-4 across {self.sessions} sessions...")
        
        for session in range(self.sessions):
            click.echo(f"Planning session {session + 1}...")
            
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
                click.echo(f"Warning: No optimal grouping found for session {session + 1}, using simple allocation")
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
        click.echo(f"\n{'='*60}")
        click.echo(f"BREAKOUT ROOM ALLOCATIONS - {self.class_size} LEARNERS")
        click.echo(f"{'='*60}")
        
        for session_idx, groups in enumerate(self.session_groups):
            click.echo(f"\nSESSION {session_idx + 1}:")
            named_groups = self.translate_group_codes_to_names(groups)
            for group_idx, group in enumerate(groups):
                learner_names = sorted([self.learner_dict.get(code, code) for code in group])
                click.echo(f"  Group {group_idx + 1}: {', '.join(learner_names)}")
    
    def print_pair_matrix(self):
        """Print a matrix showing which sessions each pair worked together"""
        click.echo(f"\n{'='*60}")
        click.echo("PAIR COLLABORATION MATRIX")
        click.echo("Numbers show which sessions learners worked together")
        click.echo(f"{'='*60}")
        
        # Create header
        header = "    "
        for learner in self.learners:
            header += f"{learner:>6}"
        click.echo(header)
        
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
            click.echo(row)
    
    def print_statistics(self):
        """Print allocation statistics"""
        click.echo(f"\n{'='*60}")
        click.echo("ALLOCATION STATISTICS")
        click.echo(f"{'='*60}")

        # Count pair frequencies
        pair_counts = Counter()
        for pair, sessions in self.pair_sessions.items():
            pair_counts[len(sessions)] += 1

        total_possible_pairs = len(self.learners) * (len(self.learners) - 1) // 2
    
        # Calculate pairs that never worked together
        actual_pairs_worked = len([p for p in self.pair_sessions.values() if p])
        pair_counts[0] = total_possible_pairs - actual_pairs_worked

        click.echo(f"Total possible pairs: {total_possible_pairs}")
        click.echo(f"Pairs that never worked together: {pair_counts[0]} ({pair_counts[0]/total_possible_pairs*100:.1f}%)")
        
        for count in sorted(pair_counts.keys()):
            if count > 0:
                click.echo(f"Pairs that worked together {count} time(s): {pair_counts[count]} ({pair_counts[count]/total_possible_pairs*100:.1f}%)")
        
        # Average meetings per person
        total_meetings = sum(len(sessions) for sessions in self.pair_sessions.values())
        meetings_per_person = (total_meetings * 2) / len(self.learners)  # *2 because each meeting involves 2 people
        click.echo(f"\nAverage meetings per person: {meetings_per_person:.1f}")

@click.command()
@click.option('--class-size', required=True, type=click.IntRange(6, 18), 
              help='Number of learners in the class (6-18)')
@click.option('--sessions', default=8, type=click.IntRange(1, 20), 
              help='Number of sessions to plan (default: 8)')
@click.option('--learner-csv', default='data/groups.csv', type=click.Path(),
              help='Path to CSV file with learner names (default: data/groups.csv)')
@click.version_option(version='2.0.0')
def main(class_size, sessions, learner_csv):
    """
    Breakout Room Allocator for Apprenticeship Classes
    
    Optimises group mixing across sessions to minimise repeated pairings.
    Creates groups of 3-4 learners with detailed allocation statistics.
    
    Examples:
    
        python groups.py --class-size 12
        
        python groups.py --class-size 15 --sessions 6
        
        python groups.py --class-size 10 --learner-csv my-class.csv
    """
    click.echo("Breakout Room Allocator for Apprenticeship Classes")
    click.echo("=" * 50)
    
    # Check if CSV file exists and show appropriate message
    if learner_csv != 'data/groups.csv' and not Path(learner_csv).exists():
        click.echo(f"Warning: CSV file '{learner_csv}' not found. Using default learner codes.")
    elif learner_csv == 'data/groups.csv' and not Path(learner_csv).exists():
        click.echo(f"CSV file not found. Using default learner codes (L1, L2, etc.)")
    else:
        click.echo(f"Loading learner names from: {learner_csv}")

    # Load learner dictionary
    learner_dict = load_learner_dict_from_csv(learner_csv)
    
    click.echo(f"Class size: {class_size} learners")
    click.echo(f"Sessions: {sessions}")
    
    # Create allocator and run
    allocator = BreakoutAllocator(class_size, sessions, learner_dict)
    allocator.allocate_sessions()
    
    # Print results
    allocator.print_session_allocations()
    allocator.print_pair_matrix()  
    allocator.print_statistics()
    
    click.echo(f"\n{'='*60}")
    click.echo(f"Allocation complete! Use these groups for your {sessions} breakout sessions.")
    click.echo(f"{'='*60}")

if __name__ == "__main__":
    main()
