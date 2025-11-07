#%% Imports
import time
import zlib
import random
import matplotlib.pyplot as plt

from explore import PrimordialSoup


#%% Compressibility metric
def compress_ratio(data_bytes: bytes) -> float:
    n = len(data_bytes)
    if n == 0:
        return 1.0
    comp = zlib.compress(data_bytes, level=9)
    return len(comp) / n


#%% Initialize soup (adjust sizes as desired)
num_programs = 1000
budget = 2**13
pop_prop = 1.0
soup = PrimordialSoup(num_programs, budget=budget,mut_rate=0.00, pop_prop=pop_prop, prog_size=64)


#%% Live visualization loop
plt.ion()
fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=True, figsize=(9, 8))

xs = []
ys_ratio = []
ys_n = []
ys_avgL = []

line1, = ax1.plot([], [], lw=2)
line2, = ax2.plot([], [], lw=2)
line3, = ax3.plot([], [], lw=2)

ax1.set_title("Computational Life — Global Metrics")
ax1.set_ylabel("Compress ratio (zlib)")
ax1.set_ylim(0.0, 2.0)

ax2.set_ylabel("# Programs")

ax3.set_ylabel("Avg prog length")
ax3.set_xlabel("Iteration")

text = ax1.text(0.02, 0.95, "", transform=ax1.transAxes, va="top")
plt.show(block=False)

window = 500  # rolling window for display

try:
    t = 0
    while True:
        # evolve the soup by one step (updates programs in-place)
        soup.run_soup(1)

        # measure global metrics
        nprog = len(soup.programs)
        total_len = sum(len(p) for p in soup.programs)
        avg_len = (total_len / nprog) if nprog else 0.0
        soup_bytes = bytes(b for prog in soup.programs for b in prog)
        r = compress_ratio(soup_bytes)

        # update series
        xs.append(t)
        ys_ratio.append(r)
        ys_n.append(nprog)
        ys_avgL.append(avg_len)

        # update plots
        xview = xs[-window:]
        y1 = ys_ratio[-window:]
        y2 = ys_n[-window:]
        y3 = ys_avgL[-window:]
        line1.set_data(xview, y1)
        line2.set_data(xview, y2)
        line3.set_data(xview, y3)
        ax1.set_xlim(max(0, t - window), t + 1)
        ax2.set_xlim(max(0, t - window), t + 1)
        ax3.set_xlim(max(0, t - window), t + 1)
        # autoscale y for #programs and avg length
        if y2:
            ax2.set_ylim(min(y2)*0.9, max(y2)*1.1 + 1)
        if y3:
            ax3.set_ylim(min(y3)*0.9, max(y3)*1.1 + 1)
        text.set_text(f"iter={t}  bytes={len(soup_bytes)}  ratio={r:.3f}  n={nprog}  avgL={avg_len:.1f}")
        fig.canvas.draw()
        fig.canvas.flush_events()
        plt.pause(0.01)

        t += 1
except KeyboardInterrupt:
    pass
finally:
    plt.ioff()
    plt.show()


# %%
