import io, traceback
from rich.console import Console
from rich.columns import Columns
from rich.table import Table
from rich.cells import cell_len

print("### A) Columns(width=...) when width+padding > console width")
for W, w, pad in [(10, 20, (0,1)), (10, 9, (0,3)), (20, 30, (0,1)), (6, 4, (0,2)), (10, 20, (0,0))]:
    c = Console(file=io.StringIO(), width=W)
    try:
        c.print(Columns(["alpha", "beta", "gamma", "delta"], width=w, padding=pad))
        print("  W=%d width=%d pad=%s -> ok: %r" % (W, w, pad, c.file.getvalue()[:60]))
    except Exception as e:
        print("  W=%d width=%d pad=%s -> %s: %s" % (W, w, pad, type(e).__name__, e))

print()
print("### B) Table collapse_padding + fixed column width + box")
def render(t, W):
    c = Console(file=io.StringIO(), width=W, color_system=None)
    c.print(t)
    return c.file.getvalue().rstrip("\n").split("\n")

for padding in [(0,1,0,1), (0,1,0,3), (0,3,0,1)]:
    for pe in (True, False):
        t = Table(box=__import__("rich.box", fromlist=["ROUNDED"]).ROUNDED,
                  padding=padding, collapse_padding=True, pad_edge=pe, show_header=False)
        t.add_column(width=6)
        t.add_column(width=6)
        t.add_row("aaaaaa", "bbbbbb")
        t.add_row("c", "d")
        lines = render(t, 40)
        lens = sorted({cell_len(l) for l in lines})
        print("  pad=%s pad_edge=%s -> line cell widths %s %s" % (padding, pe, lens, "OK" if len(lens)==1 else "*** RAGGED ***"))
        for l in lines:
            print("      |%s|" % l)
        print()
