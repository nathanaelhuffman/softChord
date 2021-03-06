
import pyjd # dummy for pyjs
from pyjamas.ui.Label import Label
from pyjamas.ui.Button import Button
from pyjamas.ui.RootPanel import RootPanel
from pyjamas.ui.VerticalPanel import VerticalPanel
from pyjamas.ui.HorizontalPanel import HorizontalPanel
from pyjamas.ui.TextBox import TextBox
from pyjamas.ui.ListBox import ListBox
from pyjamas.ui.TextArea import TextArea
from pyjamas.ui.ScrollPanel import ScrollPanel
from pyjamas.ui.HTML import HTML
from pyjamas.ui import KeyboardListener
from pyjamas.JSONService import JSONProxy

import songs


class SoftChordApp:
    def onModuleLoad(self):
        """
        Gets run when the page is first loaded.
        Creates the widgets.
        """

        self.remote = DataService()
        
        main_layout = VerticalPanel()

        h_layout = HorizontalPanel()
        h_layout.setPadding(10)
        
        songlist_layout = VerticalPanel()
        
        songlist_layout.add(Label("Add New Song:"))
 	

        self.newSongTextBox = TextBox()
	self.newSongTextBox.addKeyboardListener(self)
        songlist_layout.add(self.newSongTextBox)
        
       	self.addSongButton = Button("Add Song")
	self.addSongButton.addClickListener(self)
	songlist_layout.add(self.addSongButton)

        #songlist_layout.add(Label("Click to Remove:"))

        self.songListBox = ListBox()
        self.songListBox.setVisibleItemCount(7)
        self.songListBox.setWidth("300px")
        self.songListBox.setHeight("400px")
        self.songListBox.addClickListener(self)
        songlist_layout.add(self.songListBox)
        
        self.deleteSongButton = Button("Delete")
        self.deleteSongButton.addClickListener(self)
        songlist_layout.add(self.deleteSongButton)
         
        h_layout.add(songlist_layout)
        
        #self.textArea = TextArea()
        #self.textArea.setCharacterWidth(30)
        #self.textArea.setVisibleLines(50)
        #h_layout.add(self.textArea)
        
        #self.scrollPanel = ScrollPanel(Size=("400px", "500px"))
        self.songHtml = HTML("<b>Please select a song in the left table</b>")
        #self.scrollPanel.add(self.songHtml)
        #h_layout.add(self.scrollPanel)
        h_layout.add(self.songHtml)
        
        main_layout.add(h_layout)
        
        self.status = Label()
        main_layout.add(self.status)
        
        RootPanel().add(main_layout)
        
        # Populate the song table:
        self.remote.getAllSongs(self)
    

    def onKeyUp(self, sender, keyCode, modifiers):
        pass

    def onKeyDown(self, sender, keyCode, modifiers):
        pass

    def onKeyPress(self, sender, keyCode, modifiers):
        """
        This functon handles the onKeyPress event
        """
        if keyCode == KeyboardListener.KEY_ENTER and sender == self.newSongTextBox:
            id = self.remote.addSong(self.newSongTextBox.getText(), self)
            self.newSongTextBox.setText("")

            if id<0:
                self.status.setText("Server Error or Invalid Response")

    def onClick(self, sender):
        """
        Gets called when a user clicked in the <sender> widget.
        Currently deletes the song on which the user clicked.
        """
        if sender == self.songListBox:
            song_id = self.songListBox.getValue(self.songListBox.getSelectedIndex())
            self.status.setText("selected song_id: %s" % song_id)
            id = self.remote.getSong(song_id, self)
            if id<0:
                self.status.setText("Server Error or Invalid Response")
        
	elif sender == self.addSongButton:
            id = self.remote.addSong(self.newSongTextBox.getText(), self)
            self.newSongTextBox.setText("")
            if id<0:
                self.status.setText("Server Error or Invalid Response")
 
        elif sender == self.deleteSongButton:
            # Figure out what song is selected in the table:
            song_id = self.songListBox.getValue(self.songListBox.getSelectedIndex())
            self.status.setText("delete song_id: %s" % song_id)
            id = self.remote.deleteSong(song_id, self)
            if id<0:
                self.status.setText("Server Error or Invalid Response")
    
    def onRemoteResponse(self, response, request_info):
        """
        Gets called when the backend (django) sends a packet to us.
        Populates the song table with all songs in the database.
        """
        self.status.setText("response received")
        if request_info.method == 'getAllSongs' or request_info.method == 'addSong' or request_info.method == 'deleteSong':
            self.status.setText(self.status.getText() + " - song list received")
            self.songListBox.clear()
            for item in response:
                song_id, song_num, song_title = item
                if song_num:
                    song_title = "%i %s" % (song_num, song_title)
                self.songListBox.addItem(song_title)
                self.songListBox.setValue(self.songListBox.getItemCount()-1, song_id)
        
        elif request_info.method == 'getSong':
            self.status.setText(self.status.getText() + " - song received")
            song_obj = songs.Song(response)
            self.status.setText(self.status.getText() + "; id: %i; num-chords: %i" % (song_obj.id, len(song_obj.chords) ) )
            self.songHtml.setHTML(song_obj.getHtml())
            #self.textArea.setText(song_obj.text)
        
        else:
            # Unknown response received form the server
            self.status.setText(self.status.getText() + "none!")
    
    def onRemoteError(self, code, errobj, request_info):
        message = errobj['message']
        self.status.setText("Server Error or Invalid Response: ERROR %s - %s" % (code, message))

class DataService(JSONProxy):
    def __init__(self):
        JSONProxy.__init__(self, "/services/", ["getAllSongs", "addSong", "deleteSong", "getSong"])

if __name__ == "__main__":
    """
    For running Pyjamas-Desktop.
    """
    pyjd.setup("public/softrchordapp.html")
    #pyjd.setup("http://127.0.0.1:8000/site_media/output/softchordapp.html")
    app = SoftChordApp()
    app.onModuleLoad()
    pyjd.run()

