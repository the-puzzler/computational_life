#%% Imports
import time
import zlib
import random
import statistics
import matplotlib.pyplot as plt

from soup import PrimordialSoup

# Defined opcodes and labels used across figures
OP_LABELS = ["<", ">", "{", "}", "-", "+", ".", ",", "[", "]", "_", "|", "\\"]
OP_CODES = [ord(c) for c in "<>{}-+.,[]_|:/\\^"]
CODE_IDX = {c: i for i, c in enumerate(OP_CODES)}


#%% Compressibility metric
def compress_ratio(data_bytes: bytes) -> float:
    n = len(data_bytes)
    if n == 0:
        return 1.0
    comp = zlib.compress(data_bytes, level=9)
    return len(comp) / n


#%% Initialize soup (adjust sizes as desired)
num_programs = 5000
budget = 8000
pop_prop = 1.0
soup = PrimordialSoup(num_programs, budget=budget,program_limit=128, program_cap=10_000,mut_rate=0.024, pop_prop=pop_prop, prog_size=64)


#trying something here:
cull_size = 50

#%% Live visualization loop
plt.ion()
fig, (ax1, ax2, ax3, ax4) = plt.subplots(4, 1, sharex=True, figsize=(10, 10))

xs = []
ys_ratio = []
ys_n = []
ys_avgL = []
ys_medL = []
ys_ins = []
ys_del = []
ys_spl = []
 

line1, = ax1.plot([], [], lw=2)
line2, = ax2.plot([], [], lw=2)
line3, = ax3.plot([], [], lw=2, label="avg")
line3b, = ax3.plot([], [], lw=2, linestyle='--', label="median")
line4a, = ax4.plot([], [], lw=1.5, label="inserts")
line4b, = ax4.plot([], [], lw=1.5, label="deletes")
line4c, = ax4.plot([], [], lw=1.5, label="splits")

ax1.set_title("Computational Life — Global Metrics")
ax1.set_ylabel("Compress ratio (zlib)")
ax1.set_ylim(0.0, 2.0)

ax2.set_ylabel("# Programs")

ax3.set_ylabel("Prog length")
ax3.set_xlabel("Iteration")
ax3.legend(loc="upper left")

ax4.set_ylabel("Ops per tick (log)")
ax4.set_yscale('log')
ax4.legend(loc="upper left")

text = ax1.text(0.02, 0.95, "", transform=ax1.transAxes, va="top")
plt.show(block=False)

window = 500  # rolling window for display

# secondary figure: present opcodes (bar chart)
fig_ops, ax_ops = plt.subplots(figsize=(6, 4))
bar_labels = ["inserts(|,:)", "deletes(/,\\)", "splits(_,^)"]
bar_vals = [0, 0, 0]
bars = ax_ops.bar(bar_labels, bar_vals)
ax_ops.set_title("Present Opcodes in Soup")
ax_ops.set_ylabel("Count in pool")
plt.show(block=False)

try:
    t = 0
    while True:
        # evolve the soup by one step (updates programs in-place)
        soup.run_soup(1)

        # measure global metrics
        nprog = len(soup.programs)
        total_len = sum(len(p) for p in soup.programs)
        avg_len = (total_len / nprog) if nprog else 0.0
        med_len = statistics.median((len(p) for p in soup.programs)) if nprog else 0.0
        soup_bytes = bytes(b for prog in soup.programs for b in prog)
        r = compress_ratio(soup_bytes)
        ins = getattr(soup, 'last_inserts', 0)
        dele = getattr(soup, 'last_deletions', 0)
        spl = getattr(soup, 'last_splits', 0)
        

        # update series
        xs.append(t)
        ys_ratio.append(r)
        ys_n.append(nprog)
        ys_avgL.append(avg_len)
        ys_medL.append(med_len)
        ys_ins.append(ins)
        ys_del.append(dele)
        ys_spl.append(spl)
        

        
        # update plots
        xview = xs[-window:]
        y1 = ys_ratio[-window:]
        y2 = ys_n[-window:]
        y3 = ys_avgL[-window:]
        y3b = ys_medL[-window:]
        y4a = ys_ins[-window:]
        y4b = ys_del[-window:]
        y4c = ys_spl[-window:]
        line1.set_data(xview, y1)
        line2.set_data(xview, y2)
        line3.set_data(xview, y3)
        line3b.set_data(xview, y3b)
        line4a.set_data(xview, y4a)
        line4b.set_data(xview, y4b)
        line4c.set_data(xview, y4c)
        ax1.set_xlim(max(0, t - window), t + 1)
        ax2.set_xlim(max(0, t - window), t + 1)
        ax3.set_xlim(max(0, t - window), t + 1)
        ax4.set_xlim(max(0, t - window), t + 1)
        # autoscale y for #programs and avg length
        if y2:
            ax2.set_ylim(min(y2)*0.9, max(y2)*1.1 + 1)
        if y3 or y3b:
            ymin3 = min((min(y3) if y3 else float('inf')), (min(y3b) if y3b else float('inf')))
            ymax3 = max((max(y3) if y3 else 0), (max(y3b) if y3b else 0))
            ax3.set_ylim(ymin3*0.9 if ymin3!=float('inf') else 0, ymax3*1.1 + 1)
        if y4a or y4b or y4c:
            ymax = max([max(y) for y in [y4a or [1], y4b or [1], y4c or [1]]])
            bottom = 1 if ymax >= 1 else 0.1
            ax4.set_ylim(bottom, ymax*1.1 + 1)
        text.set_text(f"iter={t}  bytes={len(soup_bytes)}  ratio={r:.3f}  n={nprog}  avgL={avg_len:.1f}")
        fig.canvas.draw()
        fig.canvas.flush_events()
        plt.pause(0.01)

        # update bar chart of present grouped opcodes in the pool
        PIPE, COLON = ord('|'), ord(':')
        SLASH, BSLASH = ord('/'), ord('\\')
        USCORE, CARET = ord('_'), ord('^')
        present_ins = present_del = present_spl = 0
        for prog in soup.programs:
            for b in prog:
                if b == PIPE or b == COLON: present_ins += 1
                elif b == SLASH or b == BSLASH: present_del += 1
                elif b == USCORE or b == CARET: present_spl += 1
        for rect, h in zip(bars, [present_ins, present_del, present_spl]):
            rect.set_height(h)
        ax_ops.relim(); ax_ops.autoscale_view()
        fig_ops.canvas.draw()
        fig_ops.canvas.flush_events()

        if cull_size != 0:
            soup.programs = soup.programs[cull_size:] + soup.init_programs(cull_size)



        t += 1
except KeyboardInterrupt:
    pass
finally:
    plt.ioff()
    plt.show()


# %%
