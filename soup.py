import random
from concurrent.futures import ProcessPoolExecutor
import os

from BFFVM import VM

def _run_one(args):
    prog, budget, program_limit = args
    vm = VM()
    new_prog, spawned = vm.run_program(prog, budget=budget, program_limit=program_limit)
    return new_prog, spawned, vm.cnt_insert, vm.cnt_delete, vm.cnt_split


class PrimordialSoup():
    def __init__(self, num_programs_init, budget = 1000,
                 program_limit = 516, 
                 pop_prop = 0.1, mut_rate=0.00, prog_size=64, program_cap = 10_000):
        self.num_programs_init = num_programs_init
        self.vm = VM()
        self.budget = budget
        self.program_limit = program_limit
        self.pop_prop = pop_prop
        self.values = [i for i in range(256)]
        self.mut_rate = mut_rate
        self.prog_size = prog_size
        self.program_cap = program_cap
        self.last_inserts = 0
        self.last_deletions = 0
        self.last_splits = 0
    
        self.programs = self.init_programs(self.num_programs_init)
        self.pool = ProcessPoolExecutor(max_workers=os.cpu_count())
        print('cpu count: ',os.cpu_count )
        
        
    def init_programs(self, num_programs_init):
        programs = []
        
        #self.SPLIT = ord('_'); self.values_init = [v for v in self.values if v != self.SPLIT]
        for _ in range(num_programs_init):
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
            ins = 0; dele = 0; spl = 0
            if chosen:
                payload = [(self.programs[i], self.budget, self.program_limit) for i in chosen]

                # use the persistent pool 
                results = list(self.pool.map(_run_one, payload, chunksize=1000))

                for (new_prog, spawned, ci, cd, cs), i in zip(results, chosen):
                    self.programs[i] = new_prog if new_prog else None 
                        
                    ins += ci; dele += cd; spl += cs
                    for s in spawned:
                        if s: 
                        
                            self.programs.append(s)
                
                self.programs = [p for p in self.programs if p]  # drops None and []

            mr = self.mut_rate
            vals = self.values
            for program in self.programs:
                for k in range(len(program)):
                    if random.random() < mr:
                        program[k] = random.choice(vals)

            if len(self.programs) > self.program_cap:
                self.programs = self.programs[- self.program_cap :]
                
            # if len(self.programs) > self.program_cap:
            #     self.programs = random.sample(self.programs, 800)
            
            #self.programs = random.sample(self.programs, int(len(self.programs) * 0.95 ))
            
                
                
            self.last_inserts = ins
            self.last_deletions = dele
            self.last_splits = spl

                
                
                
        
        
        
        
        
    
    

        
        
        
if __name__ == '__main__':
    world = PrimordialSoup(1000)
    world.run_soup(1000)
