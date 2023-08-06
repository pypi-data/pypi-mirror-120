


class menugenerator():
    def __init__(self):
        self.menu_title = ""
        self.count_type = ""
        self.count_alphabet = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o"]
        self.menu_options = [""]
        self.input_marker = "##> "

    def show_menu(self, menu_options):
        print("")
        print(self.menu_title)
        print("")

        for i in range(len(menu_options)):
            if self.count_type == "num":
                print(str(i) + ") " + menu_options[i])
            else:
                if len(menu_options) <= len(self.count_alphabet):
                    print(self.count_alphabet[i] + ") " + menu_options[i])
                else:
                    print(str(i) + ") " + menu_options[i])

        print("")
        self.answer = input(self.input_marker)

        return self.answer




# x = menugenerator()
# x.menu_title = "Please select an option: "
# # x.count_type = "num"
# # x.input_marker = "--> "
# sd = x.show_menu(["metasploit", "nmap", "xhack"])
# print(sd)
