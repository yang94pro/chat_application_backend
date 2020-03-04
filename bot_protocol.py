
from aichatbot import chat
from datetime import datetime

class Bot:
    
    def __init__(self, msg, bot_status):
        self._msg = msg
        self._bot_status = bot_status


    def _bot_activate(self): 
        self._bot_status = True
        sysmsg = {
                "author": "system",
                "commend": "Bot activated",
                "time": datetime.strftime(datetime.now(), "%Y/%m%d %H:%M:%S"),
                "type": "bot"
            }
        
        return sysmsg, self._bot_status

    def _bot_deactivate(self):
        
        self._bot_status = False
        sysmsg = {
                "author": "system",
                "commend": "Bot deactivated",
                "time": datetime.strftime(datetime.now(), "%Y/%m%d %H:%M:%S"),
                "type": "bot"
        }
        return sysmsg, self._bot_status
    


    def _sherlock (self):
        self._bot_status = True

        if "@sherlock" in self._msg:
            text = self._msg.lower().strip("@sherlock")
        else:
            text = self._msg.lower()

        bot_response = chat(text)
        botmsg = {
                "author": "sherlock_bot", 
                "commend": bot_response,
                "time": datetime.strftime(datetime.now(), "%Y/%m/%d %H:%M:%S"),
                "type": "bot"
             }
        return botmsg, self._bot_status

    def _conversion(self):
        msg_channel = []
        if not self._bot_status:
            print(str(self._bot_status) + "asdddddddddddddddddd")

            return self._bot_activate()
        elif self._msg == 'quit' and self._bot_status:
            return self._bot_deactivate()

        else:
            return self._sherlock()