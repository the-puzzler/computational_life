

class VM:
    def __init__(self):
        # state
        self.tape = []
        self.ip = 0
        self.h0 = 0
        self.h1 = 0
        self.seam = 0

        # ops & dispatch
        self.OPS = "<>{}-+.,[]_|"
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
            #ord('_'): self.op_delete_at_h1,
            #ord('|'): self.op_insert_zero_at_h1,
        }
        
    def run_program(self, program, budget=None): #program is a list of ints
        self.tape = program
        self.ip = 0
        self.h0 = 0
        self.h1 = 0
        self.running = True
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
        return
    
    def run_pair(self, A, B, budget=None):
        self.seam = len(A)
        self.run_program(list(A) + list(B), budget=budget)
        if self.seam < 0: self.seam = 0
        if self.seam > len(self.tape): self.seam = len(self.tape)
        return self.tape[:self.seam], self.tape[self.seam:]
            
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

    def op_delete_at_h1(self):
        if 0 <= self.h1 < len(self.tape):
            del self.tape[self.h1]
            if self.h1 < self.seam: self.seam = max(0, self.seam - 1)
            if self.ip >= self.h1:  # preserve logical next instruction
                self.ip -= 1
            if self.h0 >= len(self.tape): self.h0 = len(self.tape) - 1
            if self.h1 >= len(self.tape): self.h1 = len(self.tape) - 1
            if not self.tape: self.running = False  # empty → halt

    def op_insert_zero_at_h1(self):
        pos = max(self.h1, 0)
        if pos > len(self.tape): self.tape.extend([0] * (pos - len(self.tape)))
        self.tape.insert(pos, 0)
        if pos < self.seam: self.seam += 1
        if self.ip >= pos:       # preserve logical next instruction
            self.ip += 1
    
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
