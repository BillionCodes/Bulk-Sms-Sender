import tkinter
import time
import logging
import tkinter.messagebox
import tkinter.scrolledtext as ScrolledText
import sys
from tkinter import messagebox as mb
import requests


class TextHandler(logging.Handler):
    """This class allows you to log to a Tkinter Text or ScrolledText widget"""
    def __init__(self, text):
        # run the regular Handler __init__
        logging.Handler.__init__(self)
        # Store a reference to the Text it will log to
        self.text = text

    def emit(self, record):
        msg = self.format(record)
        def append():
            self.text.configure(state='normal')
            self.text.insert(tkinter.END, msg + '\n')
            self.text.configure(state='disabled')
            # Autoscroll to the bottom
            self.text.yview(tkinter.END)
        # This is necessary because we can't modify the Text from other threads
        self.text.after(0, append)
        
class SMSGUI:
    def __init__(self):
        self.SMS_LENGTH = 160                 # Max length of one SMS message
        self.MSG_COST = 0.0095
        # Twilio: Find these values at https://twilio.com/user/account
        # Ensure you remove the angle brackets! < > 
        #Create root window
        self.root = tkinter.Tk()
        #Set title of root window
        self.root.title("SMS CLIENT")
        #Create top frame
        self.top_frame = tkinter.Frame(self.root)
        #Create bottom frame
        self.bottom_frame = tkinter.Frame(self.root)
        #Create a label
        self.header = tkinter.Label(self.top_frame, text = "SMS Sending App")
        #Pack the label
        self.header.pack(side = 'top')
        #Label for sender name
        self.to = tkinter.Label(self.top_frame, text = "Sender Name: ")
        self.to.pack(side = 'left')
        self.sender = tkinter.Text(self.top_frame, height = 2, width = 20)
        self.sender.pack(side = 'left')
        #Label for TO number
        self.to = tkinter.Label(self.top_frame, text = "To: ")
        self.to.pack(side = 'left')
        self.v=tkinter.Scrollbar(self.root, orient='vertical')
        self.v.pack(side=tkinter.RIGHT, fill='y')
        #Create an entry widget for TO: number
        self.toNumber = tkinter.Text(self.top_frame, height = 5, width = 30, yscrollcommand=self.v.set)
        self.v.config(command=self.toNumber.yview)
        self.toNumber.pack(side = 'bottom')
 
        #Create an entry widget for messages
        self.to = tkinter.Label(self.bottom_frame, text = "Message: ")
        self.to.pack(side = 'left')
        self.message = tkinter.Text(self.bottom_frame, height = 5, width = 52)
        #Create carrier optionmenu
        self.options_list = [
  'uscellular',
  'sprint',
  'clicksend',
  'cellone',
  'telus',
  'alaskacommunications',
  'rogers',
  'cricket',
  'nex-tech',
  'tmobile',
  'att',
  'westernwireless',
  'freedommobile',
  'verizon',
  'republic',
  'bluskyfrog',
  'loopmobile',
  'clearlydigital',
  'comcast',
  'corrwireless',
  'cellularsouth',
  'centennialwireless',
  'carolinawestwireless',
  'southwesternbell',
  'fido',
  'ideacellular',
  'indianapaging',
  'illinoisvalleycellular',
  'alltel',
  'centurytel',
  'dobson',
  'surewestcommunications',
  'mobilcomm',
  'clearnet',
  'koodomobile',
  'metrocall2way',
  'boostmobile',
  'onlinebeep',
  'metrocall',
  'mci',
  'ameritechpaging',
  'pcsone',
  'qwest',
  'satellink',
  'threeriverwireless',
  'bluegrasscellular',
  'edgewireless',
  'goldentelecom',
  'publicservicecellular',
  'westcentralwireless',
  'houstoncellular',
  'mts',
  'suncom',
  'bellmobilitycanada',
  'northerntelmobility',
  'uswest',
  'unicel',
  'virginmobilecanada',
  'virginmobile',
  'airtelchennai',
  'kolkataairtel',
  'delhiairtel',
  'tsrwireless',
  'swisscom',
  'mumbaibplmobile',
  'vodafonejapan',
  'gujaratcelforce',
  'movistar',
  'delhihutch',
  'digitextjamacian',
  'jsmtelepage',
  'escotel',
  'sunrisecommunications',
  'teliadenmark',
  'itelcel',
  'mobileone',
  'm1bermuda',
  'o2mmail',
  'telenor',
  'mobistarbelgium',
  'mobtelsrbija',
  'telefonicamovistar',
  'nextelmexico',
  'globalstar',
  'iridiumsatellitecommunications',
  'oskar',
  'meteor',
  'smarttelecom',
  'sunrisemobile',
  'o2',
  'oneconnectaustria',
  'optusmobile',
  'mobilfone',
  'southernlinc',
  'teletouch',
  'vessotel',
  'ntelos',
  'rek2',
  'chennairpgcellular',
  'safaricom',
  'satelindogsm',
'scs900', 
'sfrfrance',
  'mobiteltanzania',
 'comviq',
  'emt', 
'geldentelecom',
  'pandtluxembourg',
 'netcom',
  'primtel',
'tmobileaustria',
 'tele2lativa', 
'umc',
  'uraltel',
 'vodafoneitaly',
  'lmt', 
'tmobilegermany',
  'dttmobile',
'tmobileuk',
 'simplefreedom',
'tim',
 'vodafone',
'wyndtell',
  'projectfi'
]
        self.value_inside = tkinter.StringVar(self.root)
        self.value_inside.set("Select a Carrier")
        self.question_menu = tkinter.OptionMenu(self.bottom_frame, self.value_inside, *self.options_list)
        #Create button
        self.send = tkinter.Button(self.bottom_frame, text = "Send SMS", command = self.sendSms)
        #pack message entry and send button
        self.message.pack(side = 'left')
        self.question_menu.pack(side = 'top')
        self.send.pack(side = 'bottom')
        # logger
        self.st = ScrolledText.ScrolledText(self.root, state='disabled')
        self.st.configure(font='TkFixedFont')
        self.st.pack(side = 'bottom')

        # Create textLogger
        self.text_handler = TextHandler(self.st)

        # Add the handler to logger
        self.logger = logging.getLogger()
        self.logger.addHandler(self.text_handler)

        # Log some messages
        self.logger.warning('> Log Messages....')
        #pack frames
        self.top_frame.pack()
        self.bottom_frame.pack()
        
        self.root.mainloop()
    def sendSms(self):
        carrier = self.value_inside.get() 
        sms = self.message.get("1.0","end")
        url = 'http://localhost:9090/text'

        # Check we read a message OK
        if len(sms.strip()) == 0:
            self.logger.warning("SMS message not specified- please Enter a message. \r\nExiting!")
            mb.showerror('error', 'You must enter a message')
            sys.exit(1)
        elif len(carrier) == 0 or carrier == 'Select a Carrier':
            #self.logger.warning('You did not select a carrier')
            mb.showerror('error', 'Please select a carrier!')
            sys.exit(1)
        else:
            self.logger.warning("> SMS message to send: \n\n{}".format(sms))

        # How many segments is this message going to use?
        segments = int(len(sms.encode('utf-8')) / self.SMS_LENGTH) + 1

        # Get all numbers from toNumber textbox and remove duplicates
        numbers = self.toNumber.get('1.0', tkinter.END).splitlines()
        numbers = list(set(numbers))
        #if bool(numbers):
         #   self.logger.warning("Recipients not specified- please Enter your numbers. \r\nExiting!")
          #  mb.showerror('error', 'You must enter recipients')
           # sys.exit(1)
        #else:
            #self.logger.warning('Total numbers of ${}', len(numbers))
        # Calculate how much it's going to cost:
        messages = len(numbers)
        cost = self.MSG_COST * segments * messages
        sendern = self.sender.get("1.0","end")
        sendern = sendern[:-1]

        self.logger.warning("> {} messages of {} segments each will be sent, at a cost of ${} to numbers using {} wireless network".format(
            messages, segments, cost, carrier))

        # Check you really want to send them
        res=mb.askquestion('Send these messages?', '> {} messages of {} segments each will be sent, at a cost of ${}, please make sure you picked the right carrier '.format(
            messages, segments, cost))
        self.root.update()
        if res == 'yes':

            counters = 0
            for num in numbers:
                counters = counters + 1
                if counters == 100:
                    self.logger.warning("> Cooling sender for a minute after 100 deliveries..")
                    self.root.update()
                    time.sleep(60)
                    self.logger.warning("> Clearing cache & logs...")
                    time.sleep(1)
                    self.logger.warning("> Resuming...")
                    time.sleep(2)
                    counters = 0
                # Send the sms text to the number from the CSV file:
                self.logger.warning("> Sending to " + num)
                try:
                    resp = requests.post(url, {
                     'number': num,
                     'message': sms,
                     'from': sendern,
                     'carrier':carrier
                    })
                    res = resp.json()
                    if res['success'] == True:
                        self.logger.warning('Message sent successfully')
                    else:
                        self.logger.warning(res)
                    #responseData = send.send_message(
                     #   {
                     #      "from": from_num,
                     #       "to": "1"+str(num),
                     #       "text": sms,
                     #       }
                     #   )
                    
                    time.sleep(0.5)
                except Exception as e:
                    self.logger.warning(e)
                    self.root.update()
                    continue
                #if responseData["messages"][0]["status"] == "0":
                 #   self.logger.warning("> Message sent successfully.")
                #else:
                 #   self.logger.warning(f"> Message failed with error: {responseData['messages'][0]['error-text']}")

        mb.showinfo('Success!', 'Messages successfully sent!')
        self.root.update()
gui=SMSGUI()


