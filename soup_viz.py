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
num_programs = 50_000
budget = 2**13
pair_prop = 0.2
soup = PrimordialSoup(num_programs, budget=budget, pair_prop=pair_prop)


#%% Live visualization loop
plt.ion()
fig, ax = plt.subplots(figsize=(8, 4))
xs, ys = [], []
line, = ax.plot([], [], lw=2)
ax.set_title("Computational Life — Soup Compressibility Over Time")
ax.set_xlabel("Iteration")
ax.set_ylabel("Compressed/Raw size ratio (zlib)")
ax.set_ylim(0.0, 2.0)
text = ax.text(0.02, 0.95, "", transform=ax.transAxes, va="top")
plt.show(block=False)

window = 500  # rolling window for display

try:
    t = 0
    while True:
        # evolve the soup by one step (updates programs in-place)
        soup.run_soup(1)

        # measure compressibility of the entire soup (all programs)
        soup_bytes = bytes(b for prog in soup.programs for b in prog)
        r = compress_ratio(soup_bytes)

        # update series and plot
        xs.append(t); ys.append(r)
        xview = xs[-window:]
        yview = ys[-window:]
        line.set_data(xview, yview)
        ax.set_xlim(max(0, t - window), t + 1)
        text.set_text(f"iter={t}  soup_bytes={len(soup_bytes)}  ratio={r:.3f}")
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
