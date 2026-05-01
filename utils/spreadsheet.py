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
    
    def find_assignments(self, name):
        ws = self.ws
        cell_list = ws.findall(name, in_column=3)
        rows = [cell.row for cell in cell_list]
        all_tasks = ws.col_values(2)
        assignments = [all_tasks[row - 1] for row in rows] # Extract values using 0-based indexing
        return assignments