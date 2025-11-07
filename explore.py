import random

from BFFVM import VM



class PrimordialSoup():
    def __init__(self, num_programs_init, budget = 1000, pair_prop = 0.1, mut_rate=0.024): # riht now budget is global, could become per program?
        self.num_programs_init = num_programs_init
        self.vm = VM()
        self.budget = budget
        self.pair_prop = pair_prop
        self.values = [i for i in range(256)]
        self.mut_rate = mut_rate
    
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
            mr = self.mut_rate
            vals = self.values
            for program in self.programs:
                for k in range(len(program)):
                    if random.random() < mr:
                        program[k] = random.choice(vals)
                
                
        
        
        
        
        
    
    

        
        
        
if __name__ == '__main__':
    world = PrimordialSoup(1000)
    world.run_soup(1000)
