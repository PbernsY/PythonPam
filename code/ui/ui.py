import sys
import os
if os.path.dirname(__file__) != '':
    os.chdir(os.path.dirname(__file__)) # This changes to the directory where ui.py was executed from

sys.path.insert(1   , '../crypto/')
sys.path.insert(1   , '../facial/')
from detection import detect
import crypto_suite
from fire_data import query_retrieve_key
from fire_data import query_retrieve_contacts
from fire_data import update_last_contacted
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *

#print(BASE_DIR)

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        '''
        This sets the title and the size of the inital UI
        ''' 
        self.title = "FileEncryption with OpenCV"
        self.top = 300
        self.left = 300
        self.width = 300
        self.height = 100
        self.InitUI()

    def InitUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.top, self.left, self.width, self.height)

        '''
        This displays the encrypt file button and sets its size.
        It also changes to the encryption window when the button is clicked
        '''
        buttonWindow1 = QPushButton('Encrypt File', self)
        buttonWindow1.setGeometry(QtCore.QRect(0, 0, 301, 50))
        
        buttonWindow1.clicked.connect(self.buttonWindow1_onClick)
        
        '''
        This displays the decrypt file button and sets its size.
        It also changes to the decryption window when the button is clicked
        '''
        buttonWindow2 = QPushButton('Decrypt File', self)
        buttonWindow2.setGeometry(QtCore.QRect(0, 49, 301, 50))
        buttonWindow2.clicked.connect(self.buttonWindow2_onClick)        

        self.show() # this shows the UI to the user.

    @pyqtSlot()
    def buttonWindow1_onClick(self):
        '''
        This switches to the encryption window
        '''
        self.cams = Window1() 
        self.cams.show()
        self.close()

    @pyqtSlot()
    def buttonWindow2_onClick(self):
        '''
        This switches to the decryption window
        '''
        self.cams = Window2() 
        self.cams.show()
        self.close()


class Window1(QDialog):
    def __init__(self, value=None, parent=None):
        super().__init__(parent)

        self.setWindowTitle('Encryption') # this sets the title of the window
        self.setWindowIcon(self.style().standardIcon(QStyle.SP_FileDialogInfoView)) # This sets the style
        self.key = None # This is used by the lookup key method and encrypt method
        self.i = 0 # This is used by the last contacted method
        label1 = QLabel(value)
        self.button = QPushButton()
        self.button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)


        layoutV = QVBoxLayout()

        '''
        This shows the encrypt file button and also triggers the encrypt_file method.
        '''

        self.encrypt_button = QPushButton(self)
        self.encrypt_button.setText('Encrypt File')
        self.encrypt_button.clicked.connect(self.encrypt_file)
        layoutV.addWidget(self.encrypt_button)

        '''
         This shows the import public key button and also triggers the import_public_key method.
        '''

        self.public_key = QPushButton(self)
        self.public_key.setText('Import Public Key')
        self.public_key.clicked.connect(self.import_public_key)
        layoutV.addWidget(self.public_key)

        '''
        This shows the look user button and also triggers the lookup_key method.
        '''

        self.user_lookup = QPushButton(self)
        self.user_lookup.setText('Lookup User')
        self.user_lookup.clicked.connect(self.lookup_key)
        layoutV.addWidget(self.user_lookup)

        '''
        This shows the last contacted button and also triggers the lookup_last_contacted method
        '''

        self.last_contact = QPushButton(self)
        self.last_contact.setText('Last contacted')
        self.last_contact.clicked.connect(self.lookup_last_contacted)
        layoutV.addWidget(self.last_contact)

        '''
        This styles the back to main menu button
        '''
        self.pushButton = QPushButton(self)
        self.pushButton.setStyleSheet('background-color: rgb(0,0,255); color: #fff')
        self.pushButton.setText('Return to main menu')
        self.pushButton.clicked.connect(self.goMainWindow)
        layoutV.addWidget(self.pushButton)

        layoutH = QHBoxLayout()
        layoutV.addLayout(layoutH)
        self.setLayout(layoutV)

    def error(self):
        '''
        This is called when the user lookup has failed.
        '''
        self.not_found =  QMessageBox()
        self.not_found.setText("User not known, please try again")
        self.not_found.setWindowTitle("Error")
        return self.not_found.exec_()

    def notify_user_success(self):
        '''
        This is called when the file has been successfully encrypted
        '''
        self.successful = QMessageBox()
        self.successful.setText("File Encrypted!")
        self.successful.setWindowTitle("Success")
        return self.successful.exec_()

    def notify_user_file_not_selected(self):
        '''
        Called by lookup key
        A prompt that tell the user the lookup was successful
        '''
        self.not_selected = QMessageBox()
        self.not_selected.setText("No file selected.")
        self.not_selected.setWindowTitle("Notice")
        return self.not_selected.exec_()

    def notify_user_lookup(self):
        '''
        Called by lookup key
        A prompt that tell the user the lookup was successful
        '''
        self.user_lookup = QMessageBox()

        self.user_lookup.setText("User lookup successful!")
        self.user_lookup.setWindowTitle("Notice")
        return self.user_lookup.exec_()


    def lookup_key(self):
        '''
        This function looks up the public key of a requested user if their username is known.
        If not the user is notifed.
        If successful the user is notifed it was successful
        the username is then added to last contacted.
        '''

        inputVal = QtWidgets.QInputDialog.getText(self,"User lookup", "Enter name of user:")
        key = query_retrieve_key(inputVal[0])
        if key == False:
            self.error()
        else:
            self.key = key
            # update firebase
            update_last_contacted(inputVal[0])
            # Notify the user it was successfule
            self.notify_user_lookup()

    def lookup_last_contacted(self):
        '''
        This shows the user who they last contacted
        It queries firebase for the list of recent contacts.
        '''
        self.user_contact = query_retrieve_contacts()
        self.list_of_contacted = QListWidget()
        self.list_of_contacted.setSelectionMode(QAbstractItemView.SingleSelection)
        self.list_of_contacted.setWindowTitle("Last contacted") 
        for user in self.user_contact:
            self.list_of_contacted.insertItem(self.i, user)
            self.i += 1
       #     self.list_of_contacted.item(0).setSelected(True)
            self.list_of_contacted.show()   
            test = self.list_of_contacted.selectedIndexes()
        self.list_of_contacted.itemSelectionChanged.connect(self.check_selection)

    def check_selection(self):
        '''
        Triggered when a user clicks within the last contacted box.
        It sets the public key to the user they want to contact.
        '''
        name = ([item.text() for item in self.list_of_contacted.selectedItems()])
        key = query_retrieve_key(name[0])
        if key == False:
            self.error()
        else:
            self.key = key
            self.notify_user_lookup_with_key(name[0])
        return

    def notify_user_lookup_with_key(self,name):
        '''
        This notifies the user if lookup was sucessful 
        '''
        self.user_lookup = QMessageBox()
        self.user_lookup.setText("Key retrieval successful!\nKey from {} selected".format(name))
        self.user_lookup.setWindowTitle("Notice")
        return self.user_lookup.exec_()

    def notify_user_not_auth(self):
        '''
        This notifies the user if authorization failed
        '''
        self.user_lookup = QMessageBox()
        self.user_lookup.setText("You are not authorised to perform this action")
        self.user_lookup.setWindowTitle("Error")
        return self.user_lookup.exec_()

    def import_public_key(self):
        '''
        This function allows the user to import a public key
        It opens up a file prompt which allows the user to select the file key.

        '''
        options = QFileDialog.Options()
        input_file, _ = QFileDialog.getOpenFileName(self,"Select public key", "","All Files (*)", options=options)
        with open(input_file) as public:
            self.key = public.read()
        print(self.key)

    def encrypt_file(self, key = None):
        '''
        This function prompts the user to select a file 
        it then calls the encrpyt function which will then encrypt the file.
        It then calls facial recognition which then either authorizes or fails
        It then prompts the user to let them know if it was successful or not.
        '''
        options = QFileDialog.Options()
        input_file, _ = QFileDialog.getOpenFileName(self,"Select file to encrypt", "","All Files (*)", options=options)

        if len(input_file) > 0:
            check = detect()
            if check == True:
                if self.key == None:
                    crypto_suite.encrypt_file(input_file)
                    self.notify_user_success()
                else:
                    crypto_suite.encrypt_file(input_file,self.key)
                    self.notify_user_success()
            else:
                self.notify_user_not_auth()
        else:
            self.notify_user_file_not_selected()
    
    def goMainWindow(self):
        '''
        This allows the user to return to the encrypt or decrypt page.
        '''
        self.cams = Window()
        self.cams.show()
        self.close() 


class Window2(QDialog):
    ''' 
    This is the decrypt page that is shown when the user clicks decrypt
    ''' 

    def __init__(self, value=None, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Decryption')# this sets the title of the window
        self.setWindowIcon(self.style().standardIcon(QStyle.SP_FileDialogInfoView)) # This sets the style

        label1 = QLabel(value)
        self.button = QPushButton()

        layoutV = QVBoxLayout()
    

        '''
        This button displays decrypt file and calls the decryption method.
        '''
        self.decrypt_button = QPushButton(self)
        self.decrypt_button.setText('Decrypt File')
        self.decrypt_button.clicked.connect(self.decrypt_file)
        layoutV.addWidget(self.decrypt_button)
        
        '''
        This sets the style of the return to menu button
        '''
        self.pushButton = QPushButton(self)
        self.pushButton.setStyleSheet('background-color: rgb(0,0,255); color: #fff')
        self.pushButton.setText('Return to main menu')
        self.pushButton.clicked.connect(self.goMainWindow)
        layoutV.addWidget(self.pushButton)

        layoutH = QHBoxLayout()
        layoutV.addLayout(layoutH)
        self.setLayout(layoutV)

    def notify_user_file_not_selected(self):
        '''
        This function is called by the decryption method which notifies the user if they 
        did not select a file.
        '''
        self.not_selected = QMessageBox()
        self.not_selected.setText("No file selected.")
        self.not_selected.setWindowTitle("Notice")
        return self.not_selected.exec_()

    def notify_user_not_auth(self):
        '''
        This notifies the user if authorization failed
        '''
        self.user_lookup = QMessageBox()
        self.user_lookup.setText("You are not authorised to perform this action")
        self.user_lookup.setWindowTitle("Error")
        return self.user_lookup.exec_()


    def notify_user_file_not_encrypted(self):
        '''
        This function is called by the decryption method which notifies the user if decryption
        cannot decrypt the file.
        '''
        self.not_selected = QMessageBox()
        self.not_selected.setText("Unable to decrypt file.")
        self.not_selected.setWindowTitle("Error")
        return self.not_selected.exec_()


    def decrypt_file(self):
        '''
        This function prompts the user to select a file to decrypt
        It then calls the facial recognition which either authorizes or denies the user.
        Depending on the facial recognition outcome it notifies the user if it was successful or unsuccessful.
        '''
        options = QFileDialog.Options()
        input_file, _ = QFileDialog.getOpenFileName(self,"Select file to decrypt", "","All Files (*)", options=options)
        
        if len(input_file) > 0:
            if detect() == True:
                try:
                    check = crypto_suite.decrypt_file(input_file)
                except OverflowError:
                    return self.notify_user_file_not_encrypted()
               
                    
                else:
                    self.notify_user_success()
            else:
                self.notify_user_not_auth()
        else:
            self.notify_user_file_not_selected()

    def notify_user_success(self):
        '''
        This is called by the decryption method above
        '''
        self.successful = QMessageBox()
        self.successful.setText("File Decrypted!")
        self.successful.setWindowTitle("Success")
        return self.successful.exec_()        



    def goMainWindow(self):
        '''
        This allows the user to go back to 
        the inital window that is shown to the user.
        '''
        self.cams = Window()
        self.cams.show()
        self.close()    


if __name__ == '__main__':
    app=QApplication(sys.argv)
    ex=Window()
    sys.exit(app.exec_())
