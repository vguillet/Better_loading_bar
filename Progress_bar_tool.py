import time
from math import modf


class Progress_bar:
    def __init__(self, max_step, bar_size=30, label=None,
                 activity_indicator=True,
                 process_count=True,
                 progress_percent=True,
                 run_time=True,
                 eta=True,
                 overwrite_setting=True,
                 bar_type="Solid",
                 activity_indicator_type="Dots",
                 rainbow_bar=False):

        # --> Initiate Progress bar
        self.overwrite_setting = overwrite_setting
        self.max_step = max_step
        self.bar_size = bar_size

        self.print_activity_indicator = activity_indicator
        self.print_process_count = process_count
        self.print_progress_percent = progress_percent
        self.print_run_time = run_time
        self.print_eta = eta

        # --> Determine bar properties based on input
        self.step = max_step/self.bar_size
        self.current = 0
        self.label = label
        self.current_indicator_pos = 0
        self.colored_bar_lock = 0

        # --> Initiate time tracker
        self.initial_start_time = time.time()
        self.start_time = self.initial_start_time
        self.run_time_lst = []

        # ---- Colours and Formatting
        # --> Setting up bar formatting
        self.rainbow_bar = rainbow_bar
        self.bar_type = bar_type
        self.indicator_type = activity_indicator_type

        # --> Setting up format library
        self.bar_dict = {"Equal": {"Full": "=",
                                   "Empty": " "},
                         "Solid": {"Full": "█",
                                   "Empty": " "},
                         "Circle": {"Full": "◉",
                                    "Empty": "◯"},
                         "Square": {"Full": "▣",
                                    "Empty": "▢"}}

        self.indicator_dict = {"Bar spinner": ["-", "\\", "|", "/"],
                               "Dots": ["   ", ".  ", ".. ", "..."],
                               "Column": ['⡀', '⡄', '⡆', '⡇', '⣇', '⣧', '⣷', '⣿'],
                               "Pie spinner": ['◷', '◶', '◵', '◴'],
                               "Moon spinner": ['◑', '◒', '◐', '◓']}

        self.colours = {"reset": "\033[0m",
                        "bold": "\033[1m",
                        "green": "\033[3;32;1m",
                        "red": "\033[31;1m",
                        "magenta": "\033[35;1m",
                        "yellow": "\033[33;1m",
                        "cyan": "\033[36;1m",
                        "blue": "\033[34;1m"}

    def update_progress(self, current=None):
        if current is not None:
            self.current = current+1
        else:
            self.current += 1

        self.run_time = round(time.time() - self.start_time, 3)
        self.run_time_lst.append(self.run_time)

        if self.overwrite_setting:
            print("\r"+self.__progress_bar, end="")
        else:
            print(self.__progress_bar)

        # --> Reset start time for next iteration
        self.start_time = time.time()

    def update_activity(self):
        if len(self.run_time_lst) == 0:
            printed_bar = self.__activity_bar
        else:
            printed_bar = self.__progress_bar

        if self.overwrite_setting:
            print("\r"+printed_bar, end="")
        else:
            print(printed_bar)

    # ===============================================================================
    # -------------------------- Loading bar properties -----------------------------
    # ===============================================================================
    @property
    def __progress_bar(self):
        return self.__activity_indicator                                  \
               + self.__label                                         \
               + self.__process_count*self.print_process_count        \
               + self.__bar                                           \
               + self.__progress_percent*self.print_progress_percent  \
               + "  "*(self.print_run_time or self.print_eta)         \
               + self.__run_time*self.print_run_time                  \
               + self.__eta*self.print_eta                            \
               + self.__process_completed_msg

    @property
    def __activity_bar(self):
        return self.__activity_indicator                                  \
               + self.__label                                           \
               + self.__process_count*self.print_process_count        \
               + self.__bar                                           \
               + self.__progress_percent*self.print_progress_percent

    @property
    def __label(self):
        if self.label is not None:
            return self.label + " "*(6 - len(self.label)) + " | "
        else:
            return ""

    @property
    def __progress_percent(self):
        if round((self.current/self.max_step)*100) == 100:
            return " - " + self.colours["green"] + \
                   self.__aligned_number(round((self.current / self.max_step) * 100), 2) + "%" + \
                   self.colours["reset"]
        return " - " + self.__aligned_number(round((self.current/self.max_step)*100), 2) + "%"

    @property
    def __process_count(self):
        return self.__aligned_number(self.current, len(str(self.max_step))) + "/" + str(self.max_step)

    @property
    def __bar(self):
        nb_of_steps = int(self.current / self.step)

        # --> Define location of colored section
        self.colored_bar_lock += 1
        if self.colored_bar_lock > nb_of_steps:
            self.colored_bar_lock = 0

        if not self.rainbow_bar:
            bar = " - ["

            # --> Create filled portion of bar
            for i in range(nb_of_steps):
                if i == self.colored_bar_lock:
                    bar = bar + self.colours["cyan"] + self.bar_dict[self.bar_type]["Full"] + self.colours["reset"]
                else:
                    bar = bar + self.bar_dict[self.bar_type]["Full"]

            bar = bar + ">"

            # --> Create empty portion of bar
            for _ in range(self.bar_size-nb_of_steps):
                bar = bar + self.bar_dict[self.bar_type]["Empty"]
            bar = bar + "]"

        else:
            rainbow_lst = [self.colours["red"], self.colours["yellow"], self.colours["green"],
                           self.colours["cyan"], self.colours["blue"], self.colours["magenta"]]
            bar = self.colours["reset"] + "]"
            rainbow = -1 + self.colored_bar_lock

            # --> Create empty portion of bar
            for _ in range(self.bar_size - nb_of_steps):
                bar = self.bar_dict[self.bar_type]["Empty"] + bar

            bar = self.colours["reset"] + ">" + bar

            # --> Create filled portion of bar
            for _ in range(nb_of_steps):
                bar = rainbow_lst[rainbow] + self.bar_dict[self.bar_type]["Full"] + bar
                rainbow -= 1
                if rainbow < -1 * len(rainbow_lst):
                    rainbow = -1
            bar = " - [" + bar
        return bar

    @property
    def __run_time(self):
        if self.current == self.max_step:
            total_run_time_str = self.__formatted_time(round(time.time() - self.initial_start_time, 3))
            if len(total_run_time_str) > 0:
                return " - " + self.colours["bold"] + "Total run time: " + self.colours["reset"] + total_run_time_str
            else:
                return ""
        else:
            run_time_str = self.__formatted_time(self.run_time)
            if len(run_time_str) > 0:
                return " - " + self.colours["bold"] + "Run time: " + self.colours["reset"] + run_time_str
            else:
                return ""

    @property
    def __eta(self):
        eta_str = self.__formatted_time(sum(self.run_time_lst)/len(self.run_time_lst) * (self.max_step-self.current))

        if len(eta_str) > 0:
            return " - " + self.colours["bold"] + "ETA: " + self.colours["reset"] + eta_str
        else:
            return ""

    @property
    def __process_completed_msg(self):
        if self.current == self.max_step:
            return " - " + self.colours["green"] + "Process Completed" + self.colours["reset"]
        else:
            return ""

    @property
    def __activity_indicator(self):
        if self.overwrite_setting is True and self.current != self.max_step:
            self.current_indicator_pos += 1
            if self.current_indicator_pos > len(self.indicator_dict[self.indicator_type])-1:
                self.current_indicator_pos = 0
            return "[" + self.colours["cyan"] + self.indicator_dict[self.indicator_type][self.current_indicator_pos] + self.colours["reset"] + "] "
        else:
            return ""

    # ===============================================================================
    # ----------------------- String formatting functions ---------------------------
    # ===============================================================================
    @staticmethod
    def monkey_patch_pass(*args, **kwargs):
        return

    def __formatted_time(self, formatted_time):

        formatted_time = [0, formatted_time]
        
        time_dict_keys = ["seconds", "minutes", "hours", "days", "years"]
        time_dict = {"seconds": {"max": 60,
                                 "current": 0,
                                 "str_count": 5},

                     "minutes": {"max": 60,
                                 "current": 0,
                                 "str_count": 2},

                     "hours": {"max": 24,
                               "current": 0,
                               "str_count": 2},

                     "days": {"max": 365,
                              "current": 0,
                              "str_count": 1},

                     "weeks": {"max": 365,
                               "current": 0,
                               "str_count": 1},

                     "months": {"max": 12,
                                "current": 0,
                                "str_count": 2},

                     "years": {"max": 10,
                               "current": 0,
                               "str_count": 1},

                     "decades": {"max": 10,
                                 "current": 0,
                                 "str_count": 2},

                     "centuries": {"max": 99999999999999999999999,
                                   "current": 0,
                                   "str_count": 5}}

        # --> Fill eta dict
        current_time_key = 0
        while formatted_time[1] / time_dict[time_dict_keys[current_time_key]]["max"] > 1:
            formatted_time = list(modf(formatted_time[1] / time_dict[time_dict_keys[current_time_key]]["max"]))
            if current_time_key == 0:
                time_dict[time_dict_keys[current_time_key]]["current"] = round(formatted_time[0] * time_dict[time_dict_keys[current_time_key]]["max"], 2)
            else:
                time_dict[time_dict_keys[current_time_key]]["current"] = round(formatted_time[0] * time_dict[time_dict_keys[current_time_key]]["max"])

            current_time_key += 1

        if current_time_key != 0:
            time_dict[time_dict_keys[current_time_key]]["current"] = round(formatted_time[1])
        else:
            time_dict[time_dict_keys[current_time_key]]["current"] = round(formatted_time[1] + formatted_time[0], 2)

        # --> Create time string
        time_str = ""
        for key in time_dict_keys:
            if time_dict[key]["current"] != 0:
                if time_dict[key]["current"] != 1:
                    time_str = self.__aligned_number(time_dict[key]["current"], time_dict[key]["str_count"], align_side="right") + " " + key + ", " + time_str
                else:
                    time_str = self.__aligned_number(time_dict[key]["current"], time_dict[key]["str_count"], align_side="right") + " " + key[:-1] + " , " + time_str

        return time_str[:-2]
    
    @staticmethod
    def __aligned_number(current, req_len, align_side="left"):
        current = str(current)

        while len(current) < req_len:
            if align_side == "left":
                current = "0" + current
            else:
                current = current + "0"
        return current


if __name__ == "__main__":
    maxi_step = 100
    "Bar type options: Equal, Solid, Circle, Square"
    "Activity indicator type options: Bar spinner, Dots, Column, Pie spinner, Moon spinner"

    bar = Progress_bar(maxi_step,
                       label="Demo bar",
                       process_count=True,
                       progress_percent=True,
                       run_time=True,
                       eta=True,
                       overwrite_setting=True,
                       bar_type="Equal",
                       activity_indicator_type="Bar spinner",
                       rainbow_bar=False)

    for i in range(maxi_step):
        for j in range(4):
            bar.update_activity()
            time.sleep(0.2)
        bar.update_progress()

