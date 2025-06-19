import time
import sys
import itertools

class ProgressBar:
    BAR_STYLES = {
        "Equal": ("=", " "),
        "Solid": ("█", " "),
        "Circle": ("◉", "◯"),
        "Square": ("▣", "▢"),
    }

    SPINNERS = {
        "Bar spinner": ["-", "\\", "|", "/"],
        "Dots": ["   ", ".  ", ".. ", "..."],
        "Column": ['⡀','⡄','⡆','⡇','⣇','⣧','⣷','⣿'],
        "Pie spinner": ['◷','◶','◵','◴'],
        "Moon spinner": ['◑','◒','◐','◓'],
        "Stack": [' ','▁','▂','▃','▄','▅','▆','▇','█'],
        "Pie stack": ['○','◔','◑','◕','●'],
    }

    COLORS = {
        "reset": "\033[0m",
        "bold":  "\033[1m",
        "green": "\033[32;1m",
        "cyan":  "\033[36;1m",
    }

    def __init__(
        self,
        max_steps,
        *,
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
        rainbow=False
    ):
        if not isinstance(max_steps, int) or max_steps <= 0:
            raise ValueError("max_steps must be a positive integer")
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
        self.show_percent = show_percent
        self.show_time    = show_time
        self.show_rate    = show_rate
        self.show_eta     = show_eta

        self.full_char, self.empty_char = self.BAR_STYLES[bar_style]
        self.spinner = itertools.cycle(self.SPINNERS[spinner_style])
        self.rainbow = rainbow

        self.start_time = time.perf_counter()
        self.last_time  = self.start_time
        self.times      = []
        self.current    = 0

    def _render_parts(self, sublabel=None):
        """Assemble all the pieces for a full bar line."""
        now = time.perf_counter()
        elapsed = now - self.last_time
        if self.current > 0:
            self.times.append(elapsed)
        self.last_time = now

        parts = []
        if self.show_spinner:
            parts.append(f"[{self.COLORS['cyan']}{next(self.spinner)}{self.COLORS['reset']}]")

        # label / sublabel
        if self.label or sublabel:
            lbl = self.label
            if sublabel:
                lbl = f"{lbl}: {sublabel}" if lbl else sublabel
            parts.append(lbl)

        # count
        if self.show_count:
            parts.append(f"{self.current:0{len(str(self.max))}d}/{self.max}")

        # bar
        if self.show_count or self.show_percent:
            frac   = min(self.current/self.max, 1.0)
            filled = int(self.bar_size*frac)
            bar = self.full_char*filled + self.empty_char*(self.bar_size-filled)
            if self.rainbow:
                colors = ["\033[31m","\033[33m","\033[32m",
                          "\033[36m","\033[34m","\033[35m"]
                bar = "".join(
                    f"{colors[i%len(colors)]}{c}{self.COLORS['reset']}"
                    for i,c in enumerate(bar)
                )
            parts.append(f"[{bar}]")

        # percent
        if self.show_percent:
            pct = int(100*self.current/self.max)
            col = self.COLORS["green"] if pct==100 else ""
            rst = self.COLORS["reset"] if col else ""
            parts.append(f"{col}{pct:3d}%{rst}")

        # elapsed time
        total = now - self.start_time
        if self.show_time:
            parts.append(f"⏱️ {total:.2f}s")

        # rate
        if self.show_rate and self.times:
            rate = 1/(sum(self.times)/len(self.times))
            parts.append(f"⚡ {rate:.2f} it/s")

        # ETA
        if self.show_eta and self.times and self.current < self.max:
            eta = (sum(self.times)/len(self.times))*(self.max-self.current)
            parts.append(f"⏳ {eta:.2f}s")

        # done
        if self.current >= self.max:
            parts.append(f"{self.COLORS['bold']}✔ Done{self.COLORS['reset']}")

        return " | ".join(parts)

    def update(self, step=None, sublabel=None):
        """Use in for-loops."""
        self.current = step if step is not None else self.current + 1

        # --> Print bar
        if self.overwrite:
            print(f"\r{self._render_parts(sublabel)}", end="", flush=True)
        else:
            print(self._render_parts(sublabel))

        if self.current == self.max:
            print("\n")


if __name__ == "__main__":
    # for-loop example
    pb = ProgressBar(
        50, 
        label="Loading", 
        rainbow=True
    )
    for i in range(50):
        time.sleep(0.03)
        pb.update()

    # while-loop example
    cnt = 0
    act = ProgressBar(20, label="Waiting", rainbow=False)
    while cnt < 20:
        time.sleep(0.1)
        cnt += 1
        act.update()
    print()  # final newline
