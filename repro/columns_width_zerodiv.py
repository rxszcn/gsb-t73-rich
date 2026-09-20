import io
from rich.console import Console
from rich.columns import Columns
from rich.cells import cell_len

ITEMS = ["alpha", "beta", "gamma", "delta", "eps"]


def show(label, W, **kw):
    c = Console(file=io.StringIO(), width=W)
    try:
        c.print(Columns(list(ITEMS), **kw))
    except Exception as e:
        print("  %-28s -> RAISED %s: %s" % (label, type(e).__name__, e))
        return
    out = c.file.getvalue().rstrip("\n")
    lines = out.split("\n")
    lens = sorted({cell_len(l) for l in lines})
    cols = max(sum(1 for it in ITEMS if it in l) for l in lines)
    lost = [it for it in ITEMS if not any(it in l for l in lines)]
    print("  %-28s -> rows=%d cols=%d lens=%s lost=%s" % (label, len(lines), cols, lens, lost))
    for l in lines[:4]:
        print("     |%s|" % l)


print("### A) width+padding exceeds console")
for W, w, pad in [(10, 20, (0, 1)), (10, 9, (0, 3)), (20, 30, (0, 1)), (10, 20, (0, 0))]:
    show("W=%d w=%d pad=%s" % (W, w, pad), W, width=w, padding=pad)

print("### B) fit boundary, w=8 pad=(0,1); n cols need n*8+(n-1)*1 cells")
for W in (16, 17, 18, 26, 35):
    show("W=%d w=8 pad=(0,1)" % W, W, width=8, padding=(0, 1))
show("W=100 w=16 pad=(0,1)", 100, width=16, padding=(0, 1))

print("### C) degraded modes, W=10 w=20 pad=(0,1)")
show("column_first", 10, width=20, column_first=True)
show("right_to_left", 10, width=20, right_to_left=True)
show("equal", 10, width=20, equal=True)

print("### D) fit boundary x column_first")
show("cf W=17 w=8", 17, width=8, column_first=True)
show("cf W=35 w=8", 35, width=8, column_first=True)
