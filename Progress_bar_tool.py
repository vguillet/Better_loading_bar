import time
import sys
import itertools

class ProgressBar:
    BAR_STYLES = {
        "Equal": ("=", " "),
        "Solid": ("\u2588", " "),
        "Circle": ("\u25C9", "\u25EF"),
        "Square": ("\u25A3", "\u25A2"),
    }

    SPINNERS = {
        "Bar spinner": ["-", "\\", "|", "/"],
        "Dots": ["   ", ".  ", ".. ", "..."],
        "Column": ['\u2840','\u2844','\u2846','\u2847','\u28C7','\u28E7','\u28F7','\u28FF'],
        "Pie spinner": ['\u25F7','\u25F6','\u25F5','\u25F4'],
        "Moon spinner": ['\u25D1','\u25D2','\u25D0','\u25D3'],
        "Stack": [' ','\u2581','\u2582','\u2583','\u2584','\u2585','\u2586','\u2587','\u2588'],
        "Pie stack": ['\u25CB','\u25D4','\u25D1','\u25D5','\u25CF'],
    }

    COLORS = {
        "reset": "\033[0m",
        "bold":  "\033[1m",
        "green": "\033[32;1m",
        "cyan":  "\033[36;1m",
    }

    def __init__(
        self,
        max_steps=None,
        bar_size=30,
        label=None,
        show_spinner=True,
        show_count=True,
        show_percent=True,
        show_time=True,
        show_rate=True,
        show_eta=True,
        overwrite=True,
        bar_style="Equal",
        spinner_style="Pie stack",
        rainbow=False,
        prefix="",
        suffix=""
    ):
        if max_steps is not None and (not isinstance(max_steps, int) or max_steps <= 0):
            raise ValueError("max_steps must be a positive integer or None")
        if bar_style not in self.BAR_STYLES:
            raise ValueError(f"bar_style must be one of {list(self.BAR_STYLES)}")
        if spinner_style not in self.SPINNERS:
            raise ValueError(f"spinner_style must be one of {list(self.SPINNERS)}")

        self.max        = max_steps
        self.bar_size   = bar_size
        self.label      = label or ""
        self.overwrite  = overwrite

        self.show_spinner = show_spinner
        self.show_count   = show_count
        self.show_percent = show_percent and (max_steps is not None)
        self.show_eta     = show_eta and (max_steps is not None)
        self.show_time    = show_time
        self.show_rate    = show_rate

        self.full_char, self.empty_char = self.BAR_STYLES[bar_style]
        self.spinner = itertools.cycle(self.SPINNERS[spinner_style])
        self.rainbow = rainbow

        self.start_time = time.perf_counter()
        self.last_time  = self.start_time
        self.times      = []
        self.current    = 0

        self.prefix = prefix
        self.suffix = suffix

    def _render_parts(self, sublabel=None):
        now = time.perf_counter()
        elapsed = now - self.last_time
        if self.current > 0:
            self.times.append(elapsed)
        self.last_time = now

        parts = []
        if self.show_spinner:
            parts.append(f"[{self.COLORS['cyan']}{next(self.spinner)}{self.COLORS['reset']}]")

        if self.label or sublabel:
            lbl = self.label
            if sublabel:
                lbl = f"{lbl}: {sublabel}" if lbl else sublabel
            parts.append(lbl)

        if self.show_count:
            if self.max is not None:
                parts.append(f"{self.current:0{len(str(self.max))}d}/{self.max}")
            else:
                parts.append(f"{self.current}")

        if self.show_percent or self.show_count:
            if self.max is not None:
                frac = min(self.current / self.max, 1.0)
                filled = int(self.bar_size * frac)
                bar = self.full_char * filled + self.empty_char * (self.bar_size - filled)
                if self.rainbow:
                    colors = ["\033[31m", "\033[33m", "\033[32m",
                              "\033[36m", "\033[34m", "\033[35m"]
                    bar = "".join(f"{colors[i % len(colors)]}{c}{self.COLORS['reset']}" for i, c in enumerate(bar))
                parts.append(f"[{bar}]")

        if self.show_percent and self.max is not None:
            pct = int(100 * self.current / self.max)
            col = self.COLORS["green"] if pct == 100 else ""
            rst = self.COLORS["reset"] if col else ""
            parts.append(f"{col}{pct:3d}%{rst}")

        total = now - self.start_time
        if self.show_time:
            parts.append(f"\u23F1\ufe0f Run Time: {total:.2f}s")

        if self.show_rate and self.times:
            rate = 1 / (sum(self.times) / len(self.times))
            parts.append(f"\u26A1 {rate:.2f} it/s")

        if self.show_eta and self.times and self.max is not None:
            eta = (sum(self.times) / len(self.times)) * (self.max - self.current)
            parts.append(f"\u23F3 ETA: {eta:.2f}s")

        if self.max is not None and self.current >= self.max:
            parts.append(f"{self.COLORS['bold']}\u2714 Done{self.COLORS['reset']}")

        return " | ".join(parts)

    def update(self, step=None, sublabel=None, print_bar=True) -> str:
        self.current = step if step is not None else self.current + 1

        if print_bar:
            output = f"\r{self.prefix}{self._render_parts(sublabel)}{self.suffix}"
            if self.overwrite:
                print(output, end="", flush=True)
            else:
                print(output)

            if self.max and self.current == self.max:
                print("\n")

        return self._render_parts(sublabel)

if __name__ == "__main__":
    # for-loop example
    pb = ProgressBar(50, label="Loading", rainbow=True)
    for i in range(50):
        time.sleep(0.03)
        pb.update()

    # infinite-style while-loop example
    cnt = 0
    act = ProgressBar(None, label="Waiting", rainbow=False, prefix="  !!! ", suffix=" !!!")
    while cnt < 20:
        time.sleep(0.1)
        cnt += 1
        act.update()
