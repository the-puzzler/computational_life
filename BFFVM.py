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
_ split at instruciton pointer (left kept, right spawned)
| insert value at head1 from head0 (shift right)
\\ delete at head1 (slide left)



"""

class VM:
    def __init__(self):
        # state
        self.tape = []
        self.ip = 0
        self.h0 = 0
        self.h1 = 0
        self.seam = 0
        self.spawned = []
        self.cnt_insert = 0
        self.cnt_delete = 0
        self.cnt_split = 0
        

        # ops & dispatch
        self.OPS = "<>{}-+.,[]_|/\\"
        self.OPCODES = {ord(c): c for c in self.OPS}
        self.dispatch = {
            ord('<'): self.op_left_h0,
            ord('>'): self.op_right_h0,
            ord('{'): self.op_left_h1,
            ord('}'): self.op_right_h1,
            ord('-'): self.op_dec_h0,
            ord('+'): self.op_inc_h0,
            ord('.'): self.op_copy_h0_to_h1,
            ord(','): self.op_copy_h1_to_h0,
            ord('['): self.op_jump_fwd_if_zero,
            ord(']'): self.op_jump_back_if_nonzero,
            ord('_'): self.op_split,
            ord('|'): self.op_insert_h0_at_h1,
    
           
            ord('\\'): self.op_delete_at_h1,
            
        }
        
    def run_program(self, program, budget=None, program_limit=516): #program is a list of ints
        self.tape = program
        self.ip = 0
        self.h0 = 0
        self.h1 = 0
        self.running = True
        self.spawned = []
        self.cnt_insert = 0
        self.cnt_delete = 0
        self.cnt_split = 0
        self.program_limit = program_limit
        
        steps = 0


        while self.running and 0 <= self.ip < len(self.tape):
            b = self.tape[self.ip]
            op = self.dispatch.get(b, self.nop)
            self.jumped = False
            op()
            if not self.running:
                break
            steps += 1
            if budget is not None and steps >= budget:
                self.running = False; break
            if not self.jumped: self.ip += 1
        return self.tape, self.spawned
    
            
    # ---- ops (stubs; fill in later) ----
    def nop(self): pass
    def op_left_h0(self): self.h0 = max(0, self.h0 - 1)
    def op_right_h0(self): self.h0 = min(max(len(self.tape) - 1, 0), self.h0 + 1)
    def op_left_h1(self): self.h1 = max(0, self.h1 - 1)
    def op_right_h1(self): self.h1 = min(max(len(self.tape) - 1, 0), self.h1 + 1)
    def op_dec_h0(self): self.tape[self.h0] = (self.tape[self.h0] - 1) & 0xFF
    def op_inc_h0(self): self.tape[self.h0] = (self.tape[self.h0] + 1) & 0xFF
    def op_copy_h0_to_h1(self): self.tape[self.h1] = self.tape[self.h0]
    def op_copy_h1_to_h0(self): self.tape[self.h0] = self.tape[self.h1]

    def op_jump_fwd_if_zero(self):
        if self.tape[self.h0] == 0:
            j = self.find_matching_forward(self.ip)
            if j is None: self.running = False; return
            self.ip = j
            self.jumped = True

    def op_jump_back_if_nonzero(self):
        if self.tape[self.h0] != 0:
            j = self.find_matching_backward(self.ip)
            if j is None: self.running = False; return
            self.ip = j
            self.jumped = True

    def op_split(self):
        pos = self.ip
        
        right = self.tape[pos + 1:] # + 1 means split is part of the old program.
        left = self.tape[:pos + 1]
        self.tape = left
        if len(right) >= 1 and (right[0] != ord('_')):
            self.spawned.append(right) # if the program outputs nothing, then nothing enters spawn pool
            
    
            if left[0] == ord('_'):
                self.tape = []
            
            self.cnt_split += 1
            
        self.running = False

    

    def op_insert_h0_at_h1(self):
        # Insert value from h0 to the RIGHT of h1.
        # If h1 is off the right end, do nothing.
        if not (0 <= self.h1 < len(self.tape)):
            return

        pos = self.h1 + 1  # right of h1 (append if h1 is last)
        val = self.tape[self.h0] if 0 <= self.h0 < len(self.tape) else 0

        if len(self.tape) < self.program_limit:
            self.tape.insert(pos, val)
            self.cnt_insert += 1
            


    def op_delete_at_h1(self):
        pos = self.h1
        if 0 <= pos < len(self.tape):
            del self.tape[pos]
            self.cnt_delete += 1
            if pos < self.seam: self.seam = max(0, self.seam - 1)
            if self.ip >= pos: self.ip -= 1
            if self.h0 >= len(self.tape): self.h0 = max(len(self.tape) - 1, 0)
            if self.h1 >= len(self.tape): self.h1 = max(len(self.tape) - 1, 0)
            if not self.tape: self.running = False
    
    def find_matching_forward(self, pos):
        depth = 1
        i = pos + 1
        while i < len(self.tape):
            b = self.tape[i]
            if b == ord('['):
                depth += 1
            elif b == ord(']'):
                depth -= 1
                if depth == 0:
                    return i + 1
            i += 1
        return None

    def find_matching_backward(self, pos):
        depth = 1
        i = pos - 1
        while i >= 0:
            b = self.tape[i]
            if b == ord(']'):
                depth += 1
            elif b == ord('['):
                depth -= 1
                if depth == 0:
                    return i + 1
            i -= 1
        return None
