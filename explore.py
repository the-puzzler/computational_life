import random


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
_ deletion tape[head1] (next position slides under the pointer if it exists)
| insertion tape[head1] (inserts so that the current element at pointer becomes the next element.)

"""


class PrimordialSoup():
    def __init__(self, num_programs_init, budget = 256, pair_prop = 0.1):
        self.num_programs_init = num_programs_init
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
        chosen = random.sample(self.programs, int(len(self.programs) * self.pair_prop))
        random.shuffle(chosen)
        return list(zip(chosen[::2], chosen[1::2])) #silent drop of odd program at end if exist due to zip
    
    def run_programs(self):
        b = self.budget
        
        pairs = self.sample_program_pairs()
        for pair in pairs:
            instruct_i = 0
            head0_i = 0
            head1_i = 0
            concat_program = pair[0] + pair[1]
            running = True
            while running:
                instruct 
        
        
    
    

        
        
        
        
world = PrimordialSoup(100_000)
print(len(world.programs))