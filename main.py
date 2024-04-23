#main.py
### Imports ###
import sys

from PyQt6.QtWidgets import (QPushButton, QGroupBox, QCheckBox,
                             QDialog, QHBoxLayout, QVBoxLayout,
                             QApplication, QMainWindow, QInputDialog, QWidget)

from PyQt6.QtCore import Qt

# from rich import print
# from rich.traceback import install
# install(show_locals=True)
# from rich.console import Console
# console = Console()

### Data ###



### Main Window Class ###
class MainWin(QMainWindow): # Creating a copy of the QMainWindow class that we can modify
    def __init__(self): # Responsible for building the object
        super().__init__() # Passes information back to our parent class QMainWindow

        self.tasks_todo = [] #TODO Update name
        self.tasks_complete = [] #TODO Add new list

        self.setup_ui() # Initialize the basic user interface

        self.load_tasks_from_file("tasks_todo.txt", self.lyt_tasks_main, self.tasks_todo) #TODO
        self.load_tasks_from_file("tasks_complete.txt", self.lyt_completed_main, self.tasks_complete) #TODO


        self.event_handlers()

    def setup_ui(self):
        ### Window Setup ###
        self.setWindowTitle("Todo")
        self.setGeometry(100, 100, 300, 500)

        ### UI Setup ###
        ## Tasks UI
        # Widgets
        self.grpb_tasks = QGroupBox("Todo", self) # grpb == group box

        # Layouts
        self.lyt_tasks_main = QVBoxLayout()

        # Setup
        #!self.lyt_tasks_main.addWidget(self.cb_task_1)
        #!self.lyt_tasks_main.addWidget(self.cb_task_2)

        self.grpb_tasks.setLayout(self.lyt_tasks_main)

        ## Completed UI
        # Widgets
        self.grpb_completed = QGroupBox("Completed", self) # grpb == group box

        # Layouts
        self.lyt_completed_main = QVBoxLayout()

        # Setup
        self.grpb_completed.setLayout(self.lyt_completed_main)

        ## Button UI
        # Widgets
        self.btn_add = QPushButton("Add", self)
        self.btn_remove = QPushButton("Remove Completed", self)

        # Layouts
        self.lyt_btn_main = QHBoxLayout()

        # Setup
        self.lyt_btn_main.addWidget(self.btn_add)
        self.lyt_btn_main.addWidget(self.btn_remove)


        # Main Win UI
        # Widgets
        central_widget = QWidget()

        # Layouts
        self.lyt_main = QVBoxLayout()

        # Setup
        self.lyt_main.addWidget(self.grpb_tasks)
        self.lyt_main.addWidget(self.grpb_completed)
        self.lyt_main.addLayout(self.lyt_btn_main)

        central_widget.setLayout(self.lyt_main)
        self.setCentralWidget(central_widget)


    def event_handlers(self):
        self.btn_add.clicked.connect(self.new_task)
        self.btn_remove.clicked.connect(self.remove_task)


    def new_task(self):
        txt, btn_state = QInputDialog.getText(self, "New Task", "Enter your task:")
        if btn_state and txt:
            cb_task = QCheckBox(txt, self)
            cb_task.stateChanged.connect(lambda: self.move_task(cb_task))
            self.lyt_tasks_main.addWidget(cb_task)
            self.tasks_todo.append(cb_task) #TODO: Update list name

            # Save changes to file
            self.save_tasks_to_file(self.tasks_todo, "tasks_todo.txt") #TODO


    def move_task(self, cb_task): #TODO Rewrite
        if cb_task.isChecked(): # When task is checked
            if cb_task in self.tasks_todo:
                # Remove from todo
                self.lyt_tasks_main.removeWidget(cb_task)
                self.tasks_todo.remove(cb_task)

                # Add to completed
                self.lyt_completed_main.addWidget(cb_task)
                self.tasks_complete.append(cb_task)

        else: # When tasks is unchecked
            if cb_task in self.tasks_complete:
                # Remove from completed
                self.lyt_completed_main.removeWidget(cb_task)
                self.tasks_complete.remove(cb_task)

                # Add to todo
                self.lyt_tasks_main.addWidget(cb_task)
                self.tasks_todo.append(cb_task)

        # Save changes to file
        self.save_tasks_to_file(self.tasks_todo, "tasks_todo.txt")
        self.save_tasks_to_file(self.tasks_complete, "tasks_complete.txt")

        print(f"Todo list length: {len(self.tasks_todo)}")
        print(f"Complete list length: {len(self.tasks_complete)}")
        print("----------------------------")


    # To simplify the code you have to click Remove Task for each task that needs deleting
    def remove_task(self):
        for cb_task in self.tasks_complete: #TODO: Update list name
            if cb_task.parent() == self.grpb_completed:
                self.lyt_completed_main.removeWidget(cb_task)
                self.tasks_complete.remove(cb_task) #TODO: Update list name
                cb_task.deleteLater()
        
        # Save changes to file
        self.save_tasks_to_file(self.tasks_complete, "tasks_complete.txt") #TODO


    # def remove_task(self): #TODO: Bonus to clean up task removal bugs
    #     tasks_to_remove = [cb_task for cb_task in self.tasks_complete if cb_task.parent() == self.grpb_completed]
    #     for cb_task in tasks_to_remove:
    #         self.lyt_completed_main.removeWidget(cb_task)
    #         self.tasks_complete.remove(cb_task)
    #         cb_task.deleteLater()

    #     self.save_tasks_to_file(self.tasks_complete, "tasks_complete.txt")

    
    def save_tasks_to_file(self, tasks_list, filename): #TODO
        with open(filename, 'w') as file:
            for task in tasks_list: # :Loop through the tasks list writing each task to file
                file.write(task.text() + '\n') # Move the cursor to a new line ('n/') for the next task
 

    def load_tasks_from_file(self, filename, lyt_category, lst_category): #TODO
        with open(filename, 'r') as file:
            lines = file.readlines() # Read each line in the file and add to a list
            for line in lines: # Loop though each line in the list
                task = QCheckBox(line.strip(), self) # Make a QCheckBox and use the current lines text as the name
                task.stateChanged.connect(lambda state, task=task: self.move_task(task)) # Connect it to the move_task() method
                if lst_category is self.tasks_complete: # Check if task came from complete
                    task.setChecked(True) # Set the state to 'Checked'
                lyt_category.addWidget(task) # Add the widget to the screen
                lst_category.append(task) # Append the widget to the list

### App Execution ###
if __name__ == '__main__':
    app = QApplication(sys.argv) # The app object is the engine of our application
    app.setStyle("Windows") # Set the color theme of the app to match your windows color theme
    main_win = MainWin() # The frame our app goes in
    main_win.show() # Show the main window on the screen
    sys.exit(app.exec()) # This handles closing the app when the user click the close button