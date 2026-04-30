import gspread
from datetime import date

class Sheet:
    def __init__(self):
        gc = gspread.service_account(filename=r"utils\assignment-tracker-494911-53d08f71bab7.json")
        self.ws = gc.open("assignments-sheet").sheet1

    def new_assignment(self, assignment, name, priority):
            ws = self.ws
            id_values = ws.col_values(1)
            numeric_values = [int(v) for v in id_values[1:] if v.isdigit()] # convert each value to int, skipping the header
            append_id = max(numeric_values) + 1 if numeric_values else 1
            self.ws.append_row([append_id, assignment, name, priority, str(date.today()), "No"])
            return "Updated Successfully", append_id

    def update_status(self, id, status: bool):
        cell = self.ws.find(str(id), in_column=1)
        if not cell:
            return f"Failed:Assignment with ID {id} does not exist"
        row_number = cell.row
        self.ws.update_cell(row_number, 6, "Yes" if status else "No")
        return "Updated successfully"