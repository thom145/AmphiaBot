import tkinter as tk
from datetime import datetime

from PIL import Image, ImageTk

from Agenda import agenda_events
from Email import sendemail
from Schedule import download_schedule, schedule_info

E = tk.E
W = tk.W
N = tk.N
S = tk.S


class App(tk.Frame):
    """Create window which will hold other windows"""
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)
        self.grid(sticky=N+S+E+W)

        top = self.winfo_toplevel()
        top.rowconfigure(0, weight=1)
        top.columnconfigure(0, weight=1)

        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)
        self.__create_widgets()

    def __create_widgets(self):
        """Creates other windows which will be returned into the parent frame"""
        # contains all information about schedule
        self.frame_1 = ScheduleFrame(self, bg='#D5EEFD')

        # contains all information about email
        self.frame_2 = EmailFrame(self, bg='#D0EDFE')

        # exit application
        self.frame_3 = ExitFrame(self, bg='#c9eafc')


class ScheduleFrame(tk.Frame):
    """Frame which contains all the information for the schedule.
    This includes but isn't limited to downloading the schedule, getting position
    of the user, and uploading data to agenda
    """
    def __init__(self, parent, cnf={}, **kw):
        tk.Frame.__init__(self, parent, cnf, **kw)
        self.grid(row=0, sticky=N+S+E+W)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Schedule: (text)
        self.text_schedule = tk.Text(self, height=1, width=10)
        self.text_schedule.insert(tk.END, ' Schedule:')
        self.text_schedule.config(state=tk.DISABLED,
                                  background='#D5EEFD',
                                  highlightbackground='#D5EEFD',
                                  font='helvetica 18 bold')
        self.text_schedule.grid(row=0, column=0, pady=10, padx=20, sticky=W)

        # Option menu for choosing month
        ScheduleFrame.tkvar1 = tk.StringVar(self)
        choices = ['januari', 'februari', 'maart', 'april',
                   'mei', 'juni', 'juli', 'augustus', 'september',
                   'oktober', 'november', 'december']
        ScheduleFrame.tkvar1.set(choices[datetime.now().month - 1]) # set the default option
        self.pop_up_month = tk.OptionMenu(self, ScheduleFrame.tkvar1, *choices)
        self.pop_up_month.configure(background='#D5EEFD')
        self.pop_up_month.grid(row=1, column=0, pady=10, padx=(40, 0), sticky=W)

        # Add to calendar button runs function get_schedule
        self.add_calendar = tk.Button(self,
                                      text="Add to calendar",
                                      width=15,
                                      command=get_schedule,
                                      highlightbackground='#D5EEFD')
        self.add_calendar.grid(row=1, column=0, sticky=E, padx=(0, 245))

        # Update calendar button runs function Update_Schedule
        self.update_calendar = tk.Button(self,
                                         text="Update calendar",
                                         width=15,
                                         command=update_schedule,
                                         highlightbackground='#D5EEFD')
        self.update_calendar.grid(row=2, column=0, sticky=E, padx=(0, 245), pady=5)

        # Logo of companay
        self.img = ImageTk.PhotoImage(Image.open("gif.gif"))
        self.panel = tk.Label(self, image=self.img, background='#D5EEFD')
        self.panel.place(x=375, y=18)


class EmailFrame(tk.Frame):
    """Frame which contains all the information about emailing.
    This includes but isn't limited to getting the information to mail
    and sending the actual email to a specific person.
    """
    def __init__(self, parent, cnf={}, **kw):
        tk.Frame.__init__(self, parent, cnf, **kw)
        self.grid(row=1, sticky=N+S+E+W)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        # Mail: (text)
        self.text_mail = tk.Text(self, height=1, width=10)
        self.text_mail.insert(tk.END, ' Mail:')
        self.text_mail.config(state=tk.DISABLED,
                              background='#D0EDFE',
                              highlightbackground='#D0EDFE',
                              font='helvetica 18 bold')
        self.text_mail.grid(row=0, column=0, padx=20, sticky=W+N)

        # Option menu for choosing email to send
        EmailFrame.tkvar2 = tk.StringVar(self)
        email_choices = ['Shift change', 'Day off']
        EmailFrame.tkvar2.set(email_choices[0]) # set the default option
        self.pop_up_email = tk.OptionMenu(self, EmailFrame.tkvar2, *email_choices)
        self.pop_up_email.configure(background='#D0EDFE', width=12)
        self.pop_up_email.grid(row=1, column=1, padx=(0, 20), sticky=E+N)

        # Option menu for choosing person to send to
        EmailFrame.tkvar3 = tk.StringVar(self)
        to_email = ['Email John', 'Email De Neus', 'Email Vinny',
                    'Email Sjon en De Neus', 'Email Sjon en Vinny',
                    'Email De Neus en Vinny']
        EmailFrame.tkvar3.set(to_email[0]) # set the default option
        self.pop_up_send_to = tk.OptionMenu(self, EmailFrame.tkvar3, *to_email)
        self.pop_up_send_to.configure(background='#D0EDFE', width=18)
        self.pop_up_send_to.grid(row=1, column=2, padx=(7, 25), sticky=E+N)

        # Text frame which is used to show information needed to send email
        EmailFrame.Bot_Text = tk.Text(self, width=45, height=7)
        EmailFrame.Bot_Text.grid(row=2, column=0, columnspan=2, padx=(40, 0), sticky='E')

        # Button to show the information needed to send email
        create_email_text = tk.Button(self,
                                      text='Set up email',
                                      command=get_info,
                                      width=15,
                                      highlightbackground='#d6e8ff')
        create_email_text.grid(row=3, column=1, pady=3, padx=(5, 0))

        # Button which will email the infromation
        send_email = tk.Button(self,
                               text='Send',
                               command=return_info,
                               width=15,
                               highlightbackground='#d6e8ff')
        send_email.grid(row=3, column=2)


class ExitFrame(tk.Frame):
    """Frame which is used to close the app by clicking the Quit button."""
    def __init__(self, parent, cnf={}, **kw):
        tk.Frame.__init__(self, parent, cnf, **kw)
        self.grid(row=2, sticky=N+S+E+W)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # exit button
        self.quit_button = tk.Button(self, text="Quit", command=self.quit)
        self.quit_button.configure(highlightbackground='#c9eafc')
        self.quit_button.grid(row=0, column=0, sticky=E+W, pady=(5, 0))


def get_schedule():
    """Get days and shifts and add these to calendar"""
    month = ScheduleFrame.tkvar1.get() # get month to download
    download_schedule.download_schedule(month) # download schedule from website
    schedule_info.run_all(month)
    schedule_info.get_co_workers(month)
    agenda_events.insert_events(month)


def update_schedule():
    """Removes old data and add add "new" data to calendar"""
    month = ScheduleFrame.tkvar1.get()
    agenda_events.delete_events(month)
    get_schedule()


def get_info():
    """Show the information that is needed to send the email."""
    if EmailFrame.tkvar2.get() == 'Shift change':
        EmailFrame.Bot_Text.delete('1.0', tk.END)
        ans = ('Vul de volgende gegevens in:\nHuidige dienst: \nNieuwe dienst:'
               '\nHuidige datum: \nNieuwe datum: \nRuilen met: ')
        EmailFrame.Bot_Text.insert(tk.INSERT, ans)
    else:
        EmailFrame.Bot_Text.delete('1.0', tk.END)
        ans = 'Vul de volgende gegevens in:\nVrije dag(en): \n'
        EmailFrame.Bot_Text.insert(tk.INSERT, ans)


def return_info():
    """Get the information the user entered. Use this information
    for creating and sending email.
    """
    if EmailFrame.tkvar2.get() == 'Shift change':
        inputs = EmailFrame.Bot_Text.get("1.0", 'end-1c')
        information = inputs.split()
        current_shift = information[7]
        new_shift = information[10]
        current_date = information[13]
        new_date = information[16]
        name_co_worker = information[19]
        sendemail.change_shift_different_day(current_shift,
                                             new_shift,
                                             current_date,
                                             new_date,
                                             name_co_worker)
    else:
        inputs = EmailFrame.Bot_Text.get("1.0", 'end-1c')
        information = inputs.split()
        days = information[7]
        sendemail.vacation_day(days)


def main():
    app = App()
    app.master.title("ChatBot")
    app.master.geometry("600x400")
    app.master.resizable(0, 0)
    app.mainloop()


if __name__ == "__main__":
    main()
