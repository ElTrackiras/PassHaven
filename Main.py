from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from functools import partial
import random
from win32api import GetSystemMetrics
from kivy.clock import Clock

Window.size = (GetSystemMetrics(0) * .4, GetSystemMetrics(1) * .5)
Window.top = GetSystemMetrics(0) * .15
Window.left = GetSystemMetrics(1) * .5
Builder.load_file('Assets/pass_kivy.kv')


scrambled_alphabet = ['b', 'a', 'o', 'e', 'f', 'd', 'g', 'h', 'v', 'j', 'k', 'l', 'z',
                      'n', 'c', 'r', 'p', 'q', 's', 't', 'w', 'i', 'u', 'x', 'y', 'm', '@', '_', '.', '1', '2', '3',
                      '4', '5', '6', '7', '8', '9', '0', '*', '#']
scrambled_alphabet2 = ['c', 'm', 'e', 'o', 'd', 'f', 'g', 'h', 'v', 'u', 's', 'x', 'z',
                       'n', 'w', 'q', 'p', 'r', 'k', 't', 'b', 'i', 'j', 'y', 'l', 'a', '@', '_', '.', '1', '2',
                       '3', '4', '5', '6', '7', '8', '9', '0', '*', '#']

class InitialScreen(Screen):
    def __init__(self, **kwargs):
        super(InitialScreen, self).__init__(**kwargs)
        Clock.schedule_once(self.registry_status)

    def registry_status(self, event):
        with open('Assets/settings.txt', 'r') as f:
            sett = f.readline()
        print(sett.split(':')[1])
        if sett.split(':')[1] == 'False':
            self.manager.current = 'register'
        else:
            self.manager.current = 'login'


class Registry(Screen):
    register_user = ObjectProperty(None)
    register_pass = ObjectProperty(None)
    master_user = ''
    master_pass = ''

    def register(self):
        for i in self.register_user.text:
            for j in scrambled_alphabet:
                if i.lower() == j:
                    if i.isupper():
                        self.master_user += '$&=' + str(scrambled_alphabet.index(j))
                    else:
                        self.master_user += '$#=' + str(scrambled_alphabet.index(j))

        for i in self.register_pass.text:
            for j in scrambled_alphabet2:
                if i.lower() == j:
                    if i.isupper():
                        self.master_pass += '$&=' + str(scrambled_alphabet2.index(j))
                    else:
                        self.master_pass += '$#=' + str(scrambled_alphabet2.index(j))
        with open('Assets/master_account.txt', 'w') as f:
            f.write('username:' + self.master_user + '\n' + 'password:' + self.master_pass)
        with open('Assets/settings.txt', 'w') as f:
            f.write('registered:True')

        with open('Assets/settings.txt', 'r') as f:
            status = f.readline()
        if status.split(':')[1] == 'True':
            self.manager.current = 'login'


class MasterLogin(Screen):
    user_field = ObjectProperty(None)
    pass_field = ObjectProperty(None)
    username_entered = ''
    password_entered = ''

    def login(self):
        for i in self.user_field.text:
            for j in scrambled_alphabet:
                if i.lower() == j:
                    if i.isupper():
                        self.username_entered += '$&=' + str(scrambled_alphabet.index(j))
                    else:
                        self.username_entered += '$#=' + str(scrambled_alphabet.index(j))

        for i in self.pass_field.text:
            for j in scrambled_alphabet2:
                if i.lower() == j:
                    if i.isupper():
                        self.password_entered += '$&=' + str(scrambled_alphabet2.index(j))
                    else:
                        self.password_entered += '$#=' + str(scrambled_alphabet2.index(j))

        master_account_text_file = open("Assets/master_account.txt", "r")
        user = [i for i in master_account_text_file]
        username = user[0].split(':')
        password = user[1].split(':')
        master_account_text_file.close()
        if username[1].replace('\n', '') == self.username_entered and\
                password[1].replace('\n', '') == self.password_entered:
            self.manager.get_screen('account_management').start()
            self.manager.current = 'account_management'
            self.manager.transition.direction = 'left'
        self.user_field.text = ''
        self.pass_field.text = ''
        self.username_entered = ''
        self.password_entered = ''


class AccountManagement(Screen):
    account_for = ObjectProperty(None)
    new_user = ObjectProperty(None)
    new_pass = ObjectProperty(None)
    accounts_view = ObjectProperty(None)

    def start(self):
        self.accounts_view.clear_widgets()
        scroll_grid = GridLayout(cols=1, spacing=100, size_hint_y=None, size=(self.size[0], self.size[1]))
        scroll_grid.bind(minimum_height=scroll_grid.setter('height'))

        # scroll_grid.add_widget(Button(text='ha', size_hint_y=None, size=self.accounts_view.size))
        accounts_storage = open("Assets/accounts_stored.txt", "r")
        accounts = [i.replace('\n', '').split('^') for i in accounts_storage]
        for i in accounts:
            grid_format = GridLayout(cols=1, spacing=0, size_hint_y=None)
            grid_format.bind(minimum_height=grid_format.setter('height'))
            grid_format.add_widget(Label(text='', size_hint_y=None, size_hint_x=0.9,
                                         halign='center', height=30))
            grid_acc_for = BoxLayout(orientation='horizontal')
            grid_acc_for.add_widget(Label(text='Account for: ' + i[0], size_hint_y=None, size_hint_x=0.5,
                                          halign='center', height=30))
            option_btn = Button(text='Del', size_hint_y=None, halign='center',
                                valign='center', height=30, size_hint_x=0.05)
            option_btn.bind(on_release=partial(self.account_option, i[0], i[1], i[2]))
            grid_acc_for.add_widget(option_btn)
            grid_format.add_widget(grid_acc_for)
            decoded_user = i[1].split('$')
            final_user = ''
            decoded_user_1 = []
            for a in decoded_user:
                if a != '':
                    decoded_user_1.append(a.split('='))
            for a in decoded_user_1:
                if a[0] == '&':
                    final_user += scrambled_alphabet[int(a[1])].upper()
                else:
                    final_user += scrambled_alphabet[int(a[1])]

            decoded_pass = i[2].split('$')
            final_pass = ''
            decoded_pass_1 = []
            for a in decoded_pass:
                if a != '':
                    decoded_pass_1.append(a.split('='))
            for x in decoded_pass_1:
                if x[0] == '&':
                    final_pass += scrambled_alphabet2[int(x[1])].upper()
                else:
                    final_pass += scrambled_alphabet2[int(x[1])]
            grid_format.add_widget(Label(text='Username: ' + final_user, size_hint_y=None, size_hint_x=0.9,
                                         halign='center', height=30))
            grid_format.add_widget(Label(text='Password: ' + final_pass, size_hint_y=None, size_hint_x=0.9,
                                         halign='center', height=30))

            scroll_grid.add_widget(grid_format)
        accounts_storage.close()

        self.accounts_view.add_widget(scroll_grid)

    def account_option(self, account_for, username, password, event):
        with open("Assets/accounts_stored.txt", "r") as f:
            accounts = f.readlines()
        with open("Assets/accounts_stored.txt", "w") as f:
            for account in accounts:
                if account.strip("\n") != account_for + '^' + username + '^' + password:
                    f.write(account)
        self.start()

    def add_account(self):
        encrypted_user = ''
        encrypted_pass = ''
        for i in self.new_user.text:
            for j in scrambled_alphabet:
                if i.lower() == j:
                    if i.isupper():
                        encrypted_user += '$&=' + str(scrambled_alphabet.index(j))
                    else:
                        encrypted_user += '$#=' + str(scrambled_alphabet.index(j))

        for i in self.new_pass.text:
            for j in scrambled_alphabet2:
                if i.lower() == j:
                    if i.isupper():
                        encrypted_pass += '$&=' + str(scrambled_alphabet2.index(j))
                    else:
                        encrypted_pass += '$#=' + str(scrambled_alphabet2.index(j))

        account_stored = open("Assets/accounts_stored.txt", "a")
        account_stored.write(self.account_for.text + '^' + encrypted_user + '^' + encrypted_pass + '\n')
        account_stored.close()

        self.account_for.text = ''
        self.new_user.text = ''
        self.new_pass.text = ''
        self.start()

    def randomize_username(self):
        randomized_user = ''
        for i in range(0, 10):
            randomized_user += random.choice(scrambled_alphabet)

        self.new_user.text = randomized_user

    def randomize_password(self):
        randomized_password = ''
        for i in range(0, 10):
            randomized_password += random.choice(scrambled_alphabet2)

        self.new_pass.text = randomized_password

    current_user = ObjectProperty(None)
    current_pass = ObjectProperty(None)
    new_master_user = ObjectProperty(None)
    new_master_pass = ObjectProperty(None)

    user_verification = ''
    pass_verification = ''
    new_user_replace = ''
    new_pass_replace = ''

    def change_password(self):
        for i in self.current_user.text:
            for j in scrambled_alphabet:
                if i.lower() == j:
                    if i.isupper():
                        self.user_verification += '$&=' + str(scrambled_alphabet.index(j))
                    else:
                        self.user_verification += '$#=' + str(scrambled_alphabet.index(j))

        for i in self.current_pass.text:
            for j in scrambled_alphabet2:
                if i.lower() == j:
                    if i.isupper():
                        self.pass_verification += '$&=' + str(scrambled_alphabet2.index(j))
                    else:
                        self.pass_verification += '$#=' + str(scrambled_alphabet2.index(j))

        print('Verified user:', self.user_verification)
        print('Verified password', self.pass_verification)

        for i in self.new_master_user.text:
            for j in scrambled_alphabet:
                if i.lower() == j:
                    if i.isupper():
                        self.new_user_replace += '$&=' + str(scrambled_alphabet.index(j))
                    else:
                        self.new_user_replace += '$#=' + str(scrambled_alphabet.index(j))

        for i in self.new_master_pass.text:
            for j in scrambled_alphabet2:
                if i.lower() == j:
                    if i.isupper():
                        self.new_pass_replace += '$&=' + str(scrambled_alphabet2.index(j))
                    else:
                        self.new_pass_replace += '$#=' + str(scrambled_alphabet2.index(j))

        print('new user:', self.new_user_replace)
        print('new pass:', self.new_pass_replace)

        with open('Assets/master_account.txt', 'r') as f:
            master_acc = [i.replace('\n', '').split(':') for i in f.readlines()]

        if self.user_verification == master_acc[0][1] and self.pass_verification == master_acc[1][1]:
            master_account_file = open("Assets/master_account.txt", "w")
            master_account_file.write('username:' + self.new_user_replace + '\n'
                                      + 'password:' + self.new_pass_replace)
            master_account_file.close()
            self.manager.current = 'login'
            self.manager.transition.direction = 'right'
        self.current_user.text = ''
        self.current_pass.text = ''
        self.new_master_user.text = ''
        self.new_master_pass.text = ''
        self.user_verification = ''
        self.pass_verification = ''
        self.new_user_replace = ''
        self.new_pass_replace = ''

    def go_back(self):
        self.manager.current = 'login'
        self.accounts_view.clear_widgets()
        self.manager.transition.direction = 'right'


class PasswordHaven(App):
    def build(self):
        # Create the screen manager
        sm = ScreenManager()
        sm.add_widget(InitialScreen(name='initial_screen'))
        sm.add_widget(Registry(name='register'))
        sm.add_widget(MasterLogin(name='login'))
        sm.add_widget(AccountManagement(name='account_management'))
        return sm


if __name__ == '__main__':
    PasswordHaven().run()

