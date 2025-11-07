import random

from BFFVM import VM



class PrimordialSoup():
    def __init__(self, num_programs_init, budget = 1000, 
                 pop_prop = 0.1, mut_rate=0.00, prog_size=64, program_cap = 10_000):
        self.num_programs_init = num_programs_init
        self.vm = VM()
        self.budget = budget
        self.pop_prop = pop_prop
        self.values = [i for i in range(256)]
        self.mut_rate = mut_rate
        self.prog_size = prog_size
        self.program_cap = program_cap
    
        self.programs = self.init_programs()
        
        
    def init_programs(self):
        programs = []
        
        #self.SPLIT = ord('_'); self.values_init = [v for v in self.values if v != self.SPLIT]
        for _ in range(self.num_programs_init):
            program = []
            for _ in range(self.prog_size):
                program.append(random.choice(self.values))
                
            programs.append(program)
        return programs
            
            
    def sample_programs(self):
        n = len(self.programs)
        k = int(n * self.pop_prop)
        if k < 1: return []
        idxs = random.sample(range(n), k)
        random.shuffle(idxs)
        return idxs
    
    def run_soup(self, steps):
        for _ in range(steps):
            chosen = self.sample_programs()
            for i in chosen:
                prog = self.programs[i]
                new_prog, spawned = self.vm.run_program(prog, budget=self.budget)
                self.programs[i] = new_prog
                for s in spawned:
                    if s: self.programs.append(s)
            mr = self.mut_rate
            vals = self.values
            for program in self.programs:
                for k in range(len(program)):
                    if random.random() < mr:
                        program[k] = random.choice(vals)
                        
            if len(self.programs) > self.program_cap:
                self.programs = self.programs[- self.program_cap :]
                
                
                
        
        
        
        
        
    
    

        
        
        
if __name__ == '__main__':
    world = PrimordialSoup(1000)
    world.run_soup(1000)
