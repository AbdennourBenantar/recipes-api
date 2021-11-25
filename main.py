from random import randrange
from fastapi import FastAPI,uvicorn,os
import openpyxl
app = FastAPI()


@app.get("/get_random_recipe")
async def Pick_recipe():
    file_num=randrange(1,4)
    file_name='./recipes'+str(file_num)+'.xlsx';
    wb = openpyxl.load_workbook(filename = file_name)
    worksheet=wb['recipes']
    excel_data = []
    i=1
    recipe_id=randrange(2,11501)
    for row in worksheet.iter_rows(min_row=recipe_id,max_row=recipe_id,max_col=10):
        row_data = []
        for cell in row:
            row_data.append(str(cell.value))
        excel_data.append(row_data)
        i=i+1
        
    return {
        "id":excel_data[0][1],
        "name":excel_data[0][0],
        "description":excel_data[0][7],
        "number_of_ingredients":excel_data[0][9],
        "ingredients":parse_string_to_list(excel_data[0][8]),
        "minutes":excel_data[0][2],
        "nutrition":parse_string_to_list(excel_data[0][4]),
        "number_of_steps":excel_data[0][5],
        "steps":parse_string_to_list(excel_data[0][6]),
        "tags":parse_string_to_list(excel_data[0][3]),
    }

def parse_string_to_list(value:str):
    value=value.replace("[","")
    value=value.replace("]","")
    value=value.replace("'","")
    value_items=value.split(",")
    value_list=[]
    for v in value_items:
        value_list.append(v)
    return value_list


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=int(os.getenv("PORT", default=5000)), log_level="info")