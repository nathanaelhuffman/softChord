from pyjamas.ui.Label import Label
from pyjamas.ui.RootPanel import RootPanel
from pyjamas.ui.VerticalPanel import VerticalPanel
from pyjamas.ui.TextBox import TextBox
from pyjamas.ui.ListBox import ListBox
from pyjamas.ui import KeyboardListener

from pyjamas.JSONService import JSONProxy


class SoftChordApp:
    def onModuleLoad(self):
        self.remote = DataService()
        panel = VerticalPanel()

        self.todoTextBox = TextBox()
        self.todoTextBox.addKeyboardListener(self)

        self.todoList = ListBox()
        self.todoList.setVisibleItemCount(7)
        self.todoList.setWidth("200px")
        self.todoList.addClickListener(self)

        panel.add(Label("Add New Song:"))
        panel.add(self.todoTextBox)
        panel.add(Label("Click to Remove:"))
        panel.add(self.todoList)

        self.status = Label()
        panel.add(self.status)

        RootPanel().add(panel)



    def onKeyUp(self, sender, keyCode, modifiers):
        pass

    def onKeyDown(self, sender, keyCode, modifiers):
        pass

    def onKeyPress(self, sender, keyCode, modifiers):
        """
        This functon handles the onKeyPress event, and will add the item in the text box to the list when the user presses the enter key.  In the future, this method will also handle the auto complete feature.
        """
        if keyCode == KeyboardListener.KEY_ENTER and sender == self.todoTextBox:
            id = self.remote.addSong(sender.getText(), self)
            sender.setText("")

            if id<0:
                self.status.setText("Server Error or Invalid Response")


    def onClick(self, sender):
        # FIXME send ID instead of title
        song_id = sender.getValue(sender.getSelectedIndex())
        self.status.setText("song_id: %s" % song_id)
        id = self.remote.deleteSong(song_id, self)
        if id<0:
            self.status.setText("Server Error or Invalid Response")

    def onRemoteResponse(self, response, request_info):
        self.status.setText("response received")
        if request_info.method == 'getAllSongs' or request_info.method == 'addSong' or request_info.method == 'deleteSong':
            self.status.setText(self.status.getText() + "HERE!")
            self.todoList.clear()
            for song in response:
                title = song[0]
                song_id = song[1]
                self.todoList.addItem(title)
                self.todoList.setValue(self.todoList.getItemCount()-1, song_id)
        else:
            self.status.setText(self.status.getText() + "none!")

    def onRemoteError(self, code, errobj, request_info):
        message = errobj['message']
        self.status.setText("Server Error or Invalid Response: ERROR %s - %s" % (code, message))

class DataService(JSONProxy):
    def __init__(self):
        JSONProxy.__init__(self, "/services/", ["getAllSongs", "addSong", "deleteSong"])

if __name__ == "__main__":
    app = SoftChordApp()
    app.onModuleLoad()
