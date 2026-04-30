import gspread
from datetime import date

class Sheet:
    def __init__(self):
        gc = gspread.service_account(filename=r"utils\assignment-tracker-494911-53d08f71bab7.json")
        self.ws = gc.open("assignments-sheet").sheet1

    def new_assignment(self, id, assignment, name, priority):
        if self.ws.find(str(id), in_column=1):
            return f"Failed: Assignment ID {id} already exists"
        else:
            self.ws.append_row([id, assignment, name, priority, str(date.today())])
            return "Updated Successfully"

    def update_status(self, id, status: bool):
        cell = self.ws.find(str(id), in_column=1)
        if not cell:
            return f"{id} does not exist"
        row_number = cell.row
        self.ws.update_cell(row_number, 6, "Yes" if status else "No")
        return "Updated successfully"