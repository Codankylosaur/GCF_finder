import tkinter as tk
LARGE_FONT_STYLE = ("Arial", 24, "bold")
SMALL_FONT_STYLE = ("Arial", 16)
DIGITS_FONT_STYLE = ("Arial", 40, "bold")
DEFAULT_FONT_STYLE = ("Arial", 20)

OFF_WHITE = "#F8FAFF"
WHITE = "#FFFFFF"
LIGHT_BLUE = ("#CCEDFF")
LIGHT_GRAY = "#F5F5F5"
LABEL_COLOR = "#25265E"

class GCF_program:
    def __init__(self):
        self.window = tk.Tk()
        self.window.wm_minsize(475, 400)
        self.window.title('GCF finder')

        self.item = []
        self.loglist = []
        self.current_numbers = ''
        self.current_expression = ''
        self.function_text = 'Enter'
        
        self.display_frame = self.create_display_frame()
        self.button_frame = self.create_buttons_frame()
        self.numbers_label, self.label = self.create_display_labels()
        self.function_button = self.create_function_button()
        self.clear_button = self.create_clear_button()
        self.undo_button = self.create_undo_button()
        self.redo_button = self.create_redo_button()

        self.digits = {7:(1, 1, 1), 8:(1, 2, 1), 9:(1, 3, 1),
                       4:(2, 1, 1), 5:(2, 2, 1), 6:(2, 3, 1),
                       1:(3, 1, 1), 2:(3, 2, 1), 3:(3, 3, 1),
                       0:(4, 1, 2)}
        self.create_digit_buttons()
        self.function_button_updater()
        self.backspace_button = self.create_backspace_button()
        self.bind()

        self.button_frame.rowconfigure(0, weight=1)
        for x in range(1, 6):
            self.button_frame.rowconfigure(x, weight=1)
            self.button_frame.columnconfigure(x, weight=1)
    def bind(self):
        self.window.bind("<Return>", lambda event: self.function())
        for key in self.digits:
            self.window.bind(str(key), lambda event, digit=key: self.add_to_expression(digit))
        self.window.bind("<BackSpace>", lambda event: self.backspace())
        self.window.bind(".", lambda enent: self.clear())
        self.window.bind("<Control-u>", lambda event: self.undo())
        self.window.bind("<Control-y>", lambda event: self.redo())
    def create_display_frame(self):
        frame = tk.Frame(self.window, height=221, bg=LIGHT_GRAY)
        frame.pack(expand=True, fill="both")
        return frame
    def create_buttons_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame
    def create_display_labels(self):
        numbers_label = tk.Label(self.display_frame, text=self.current_numbers, anchor=tk.E, bg=LIGHT_GRAY,
        fg=LABEL_COLOR, padx=24, font=SMALL_FONT_STYLE)
        numbers_label.pack(expand=True, fill="both")

        label = tk.Label(self.display_frame, text=self.current_expression, anchor=tk.E, bg=LIGHT_GRAY,
        fg=LABEL_COLOR, padx=24, font=LARGE_FONT_STYLE)
        label.pack(expand=True, fill="both")

        return numbers_label, label  
    def create_digit_buttons(self):
        for digit, grid_value in self.digits.items():
            button = tk.Button(self.button_frame, text=str(digit), bg=WHITE, fg=LABEL_COLOR, font=DIGITS_FONT_STYLE,
            borderwidth=2, command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_value[0], column=grid_value[1], columnspan=grid_value[2], sticky=tk.NSEW)
    def create_clear_button(self):
        button = tk.Button(self.button_frame, text='C', fg=WHITE, bg=LABEL_COLOR, font=DIGITS_FONT_STYLE,
        command=self.clear)
        button.grid(row=4, column=3, sticky=tk.NSEW)
        return button
    def GCF_finder(self):
        self.item.sort(reverse=True)
        count = len(self.item)
        clock = 0
        def GCF_calc(fnum, snum):
            f_num = int(fnum)
            s_num = int(snum)
            while True:
                s_numo = s_num
                if f_num % s_num != 0:
                    s_num = f_num % s_num
                    f_num = s_numo
                    continue
                else:
                    return s_num
                    break
        result = GCF_calc(self.item[clock], self.item[clock+1])
        clock += 2
        count -= 2
        if count == 0:
            return result
        else:
            while True:
                if count > 0:
                    result = GCF_calc(self.item[clock], result)
                    clock += 1
                    count -= 1
                    continue
                else:
                    return result
                    break
    def add_to_expression(self, value):
        self.function_button_updater()
        try:
            dummy = int(self.current_expression)
        except ValueError:
            self.current_expression = ''
            self.update_label()
        self.current_expression += str(value)
        self.function_button_updater
        self.update_label()
        self.function_button_updater()
        self.backspace_button_updater()
    def update_label(self):
        self.label.config(text=self.current_expression)
    def create_function_button(self):
        button = tk.Button(self.button_frame, text=self.function_text, bg=LABEL_COLOR, fg=WHITE, font=DIGITS_FONT_STYLE,
        borderwidth=2, command=self.function)
        button.grid(row=2, column=4, rowspan=2, columnspan=2, sticky=tk.NSEW)
        return button
    def update_function_button_text(self):
        self.function_button.config(text=self.function_text)
    def clear(self):
        self.item.clear()
        self.current_numbers = ''
        self.update_current_numbers()
        self.function_button_updater()
    def function(self):
        try:
            dummy = int(self.current_expression)
        except ValueError:
            self.current_expression = ''
            self.update_label()
        self.function_button_updater()
        if self.current_expression != '':
            self.item.append(self.current_expression)
            self.current_expression = ''
            self.update_label()
            number_string = ''
            for i in self.item:
                number_string = number_string + str(i)+', '
                self.current_numbers = number_string
        elif len(self.item) >= 2:
            result = str(self.GCF_finder())
            self.current_expression = 'The GCF of your numbers is '+ result
            self.current_numbers = ''
            self.item.clear()
        else:
            self.current_expression = 'Please specify at least two numbers'
            self.current_numbers = ''
            self.item.clear()
        self.function_button_updater()
        self.update_current_numbers()
        self.update_label()
        self.backspace_button_updater()
    def update_current_numbers(self):
        self.numbers_label.config(text=self.current_numbers)
    def function_button_updater(self):
        if self.current_expression == '' and len(self.item) < 2:
            self.function_button['state'] = tk.DISABLED
        else:
            self.function_button['state'] = tk.NORMAL
        if self.current_expression == '' and len(self.item) >= 2:
            self.function_text = 'Calculate'
            self.update_function_button_text()
        else:
            self.function_text = 'Enter'
            self.update_function_button_text()
    def backspace_button_updater(self):
        if self.current_expression == "The GCF of your numbers is " or self.current_expression == "Please specify at least two numbers":
            self.backspace_button["state"] = tk.DISABLED
        else:
            self.backspace_button["state"] = tk.NORMAL
    def backspace(self):
        self.current_expression = self.current_expression[0:-1]
        self.update_label()
    def create_backspace_button(self):
        button = tk.Button(self.button_frame, text='Backspace', bg=LABEL_COLOR, fg=WHITE, font=DIGITS_FONT_STYLE,
        borderwidth=2, command=self.backspace)
        button.grid(row=1, column=4,columnspan=2, sticky=tk.NSEW)
        return button
    def create_undo_button(self):
        button = tk.Button(self.button_frame, text='<', fg=WHITE, bg=LABEL_COLOR, font=DIGITS_FONT_STYLE,
        command=lambda: self.undo_redo('u'))
        button.grid(row=4, column=4, sticky=tk.NSEW)
        return button
    def create_redo_button(self):
        button = tk.Button(self.button_frame, text='>', fg=WHITE, bg=LABEL_COLOR, font=DIGITS_FONT_STYLE,
        command=lambda: self.undo_redo('r'))
        button.grid(row=4, column=5, sticky=tk.NSEW)
        return button
    def undo(self):
        if len(self.item) > 1:
            self.loglist.append(self.item[-1])
            self.item.pop(-1)
            number_string = ''
            for i in self.item:
                number_string = number_string + str(i)+', '
                self.current_numbers = number_string
                self.update_current_numbers()
        elif len(self.item) == 1:
            self.loglist.append(self.item[-1])
            self.item.pop(-1)
            self.current_numbers = ''
            self.update_current_numbers()
        else:
            return
    def redo(self):
        if len(self.loglist) > 0:
            self.item.append(self.loglist[-1])
            self.loglist.pop(-1)
            number_string = ''
            for i in self.item:
                number_string = number_string + str(i)+', '
                self.current_numbers = number_string
                self.update_current_numbers()
        else:
            return
    def undo_redo(self, mode):
        if mode == 'u':
            ap_list, pop_list = 'self.loglist', 'self.item'
            num, boole = 1, True
        else:
            ap_list, pop_list = 'self.item', 'self.loglist'
            num, boole = 0, False
        if len(eval(pop_list)) > num:
            eval(ap_list).append(eval(pop_list)[-1])
            eval(pop_list).pop(-1)
            number_string = ''
            for i in self.item:
                number_string = number_string + str(i)+', '
                self.current_numbers = number_string
                self.update_current_numbers()
        elif len(self.item) == 1 and boole == True:
            self.loglist.append(self.item[-1])
            self.item.pop(-1)
            self.current_numbers = ''
            self.update_current_numbers()
        else:
            return
    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    GCF = GCF_program()
    GCF.run()