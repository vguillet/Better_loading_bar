import time
from math import modf


class Progress_bar:
    def __init__(self, max_step=None, bar_size=30, label=None,
                 activity_indicator=True,
                 process_count=True,
                 progress_percent=True,
                 run_time=True,
                 eta=True,
                 overwrite_setting=True,
                 bar_type="Equal",
                 activity_indicator_type="Dots",
                 rainbow_bar=False):

        # --> Initiate Progress bar
        self.overwrite_setting = overwrite_setting
        self.bar_size = bar_size

        if max_step is not None:
            self.max_step = max_step
            self.step = max_step / self.bar_size
            self.current = 0
            self.progress = True
        else:
            self.max_step = 99999999999999999999
            self.step = 99999999999999999999
            self.current = 0
            self.progress = False

        self.print_activity_indicator = activity_indicator
        self.print_process_count = process_count
        self.print_progress_percent = progress_percent
        self.print_run_time = run_time
        self.print_eta = eta

        # --> Determine bar properties based on input
        self.label = label
        self.current_indicator_pos = 0
        self.colored_bar_lock = 0

        # --> Initiate time tracker
        self.initial_start_time = time.time()
        self.start_time = self.initial_start_time
        self.run_time = 0
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
                               "Moon spinner": ['◑', '◒', '◐', '◓'],
                               "Stack": [' ', '▁', '▂', '▃', '▄', '▅', '▆', '▇', '█'],
                               "Pie stack": ['○', '◔', '◑', '◕', '●']}

        self.colours = {"reset": "\033[0m",
                        "bold": "\033[1m",
                        "italic": "\033[3m",
                        "underline": "\033[4m",
                        "green": "\033[32;1m",
                        "red": "\033[31;1m",
                        "magenta": "\033[35;1m",
                        "yellow": "\033[33;1m",
                        "cyan": "\033[36;1m",
                        "blue": "\033[34;1m"}

    def update_progress(self, current=None):
        # --> Calc and record run time
        self.run_time = round(time.time() - self.start_time, 3)

        if current is not None:
            self.current = current+1
        else:
            self.current += 1

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
        return self.__activity_indicator*self.print_activity_indicator                  \
               + self.__label                                                           \
               + self.__process_count*self.print_process_count                          \
               + self.__bar*self.progress                                               \
               + self.__progress_percent*self.print_progress_percent*self.progress      \
               + "  "*(self.print_run_time or self.print_eta)                           \
               + self.__run_time*self.print_run_time                                    \
               + self.__eta*self.print_eta*self.progress                                \
               + self.__process_completed_msg*self.progress

    @property
    def __activity_bar(self):
        return self.__activity_indicator*self.print_activity_indicator                  \
               + self.__label                                                           \
               + self.__process_count*self.print_process_count                          \
               + self.__bar*self.progress                                               \
               + self.__progress_percent*self.print_progress_percent*self.progress      \
               + self.__run_time*(1-self.progress)

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
        if self.progress:
            return self.__aligned_number(self.current, len(str(self.max_step))) + "/" + str(self.max_step)
        else:
            self.current += 1
            return str(self.current) + " iterations"

    @property
    def __bar(self):
        nb_of_steps = int(self.current / self.step)
        self.colored_bar_lock += 1

        # --> Prefix of bar
        bar = " - ["
        
        # ---- Create filled portion of bar
        if not self.rainbow_bar:
            # --> Define location of colored section
            if self.colored_bar_lock > nb_of_steps:
                self.colored_bar_lock = 0

            for step in range(nb_of_steps):
                if step == self.colored_bar_lock or step == self.colored_bar_lock - 1:
                    bar = bar + self.colours["cyan"] + self.bar_dict[self.bar_type]["Full"] + self.colours["reset"]
                else:
                    bar = bar + self.bar_dict[self.bar_type]["Full"]

        else:
            rainbow_lst = [self.colours["red"], self.colours["yellow"], self.colours["green"],
                           self.colours["cyan"], self.colours["blue"], self.colours["magenta"]]

            if self.colored_bar_lock >= len(rainbow_lst):
                self.colored_bar_lock = 0

            rainbow = self.colored_bar_lock

            size = 0
            # --> Create filled portion of bar
            for _ in range(nb_of_steps):
                bar = bar + rainbow_lst[rainbow] + self.bar_dict[self.bar_type]["Full"]
                size += 1
                if size > 1:
                    rainbow += 1
                    size = 0

                if rainbow >= len(rainbow_lst):
                    rainbow = 0

        bar = bar + self.colours["reset"] + ">"

        # --> Create empty portion of bar
        for _ in range(self.bar_size - nb_of_steps):
            bar = bar + self.bar_dict[self.bar_type]["Empty"]

        # --> Suffix of bar
        bar = bar + "]"

        return bar

    @property
    def __run_time(self):
        if self.progress:
            # --> Save run time to runtime list
            self.run_time_lst.append(self.run_time)

            if self.current != self.max_step:
                # --> Create run time string
                run_time_str = self.__formatted_time(self.run_time)
            else:
                # --> Create total run time string
                total_run_time_str = self.__formatted_time(round(time.time() - self.initial_start_time, 3))
                return " - " + self.colours["bold"] + "Total run time: " + self.colours["reset"] + total_run_time_str

        else:
            # --> Calc run time
            self.run_time = round(time.time() - self.start_time, 3)

            # --> Reset start time for next iteration
            self.start_time = time.time()

            # --> Create run time string (including total run time)
            total_run_time_str = self.__formatted_time(round(time.time() - self.initial_start_time, 3))
            run_time_str = self.__formatted_time(self.run_time) + " - " + "Total run time: " + self.colours["reset"] + total_run_time_str

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
            if self.current_indicator_pos >= len(self.indicator_dict[self.indicator_type]):
                self.current_indicator_pos = 0
            return "[" + self.colours["cyan"] + self.indicator_dict[self.indicator_type][self.current_indicator_pos] + self.colours["reset"] + "] "
        else:
            return ""

    # ===============================================================================
    # ----------------------- String formatting functions ---------------------------
    # ===============================================================================
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

        # --> Fill time dict
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
    "Activity indicator type options: Bar spinner, Dots, Column, Pie spinner, Moon spinner, Stack, Pie stack"

    bar = Progress_bar(max_step=None,
                       label="Demo bar",
                       process_count=True,
                       progress_percent=True,
                       run_time=True,
                       eta=True,
                       overwrite_setting=True,
                       bar_type="Equal",
                       activity_indicator_type="Pie stack",
                       rainbow_bar=False)

    for i in range(maxi_step):
        for j in range(4):
            bar.update_activity()
            time.sleep(0.01)
        # bar.update_progress()
