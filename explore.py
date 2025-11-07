import random

from BFFVM import VM

"""
instuction pointer is a seperate head.
head0 is read
head1 is write head


< head0 = head0 - 1
> head0 = head0 + 1
{ head1 = head1 - 1
} head1 = head1 + 1
- tape[head0] = tape[head0] - 1
+ tape[head0] = tape[head0] + 1
. tape[head1] = tape[head0]
, tape[head0] = tape[head1]
[ if (tape[head0] == 0): jump forwards to matching ] command.
] if (tape[head0] != 0): jump backwards to matching [ command.    

my additions:
_ deletion tape[head1] (next position slides under the pointer if it exists)
| insertion tape[head1] (inserts so that the current element at pointer becomes the next element.)

"""


class PrimordialSoup():
    def __init__(self, num_programs_init, budget = 1000, pair_prop = 0.1): # riht now budget is global, could become per program?
        self.num_programs_init = num_programs_init
        self.vm = VM()
        self.budget = budget
        self.pair_prop = pair_prop
        self.values = [i for i in range(256)]
    
    
        self.programs = self.init_programs()
        
        
    def init_programs(self):
        programs = []
        for _ in range(self.num_programs_init):
            program = []
            for _ in range(64):
                program.append(random.choice(self.values))
            programs.append(program)
        return programs
            
            
    def sample_program_pairs(self):
        n = len(self.programs)
        k = int(n * self.pair_prop)
        if k < 2: return []
        if k % 2 == 1: k -= 1
        idxs = random.sample(range(n), k)
        random.shuffle(idxs)
        return list(zip(idxs[::2], idxs[1::2])) # indices
    
    def run_soup(self, steps):
        for _ in range(steps):
            pairs = self.sample_program_pairs()
            for i, j in pairs:
                A, B = self.programs[i], self.programs[j]
                A2, B2 = self.vm.run_pair(A, B, budget=self.budget)
                self.programs[i] = A2
                self.programs[j] = B2
                
                
        
        
        
        
        
    
    

        
        
        
if __name__ == '__main__':
    world = PrimordialSoup(1000)
    world.run_soup(1000)
