from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel
import pandas as pd
import logging
from typing import List

app = FastAPI()

FILE_NAME = 'data.xlsx'

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
"""
ADD {"name": "abc", "quantity": 3, "price":24.54 }
READ ALL {}
READ {"name": "abc"}
UPDATE {"name": "abc", "quantity": 10}
READ {"name": "abc"}
DELETE {"name": "abc"}
READ {"name": "abc"}
"""
class Item(BaseModel):
    # Define the structure of your Excel data here
    name: str
    quantity: int
    price: float

def write_excel(df: pd.DataFrame):
    """Writes the DataFrame to an Excel file, creating or overwriting the existing file."""
    try:
        df.to_excel(FILE_NAME, index=False)
        logging.info(f"Data successfully written to {FILE_NAME}.")
    except Exception as e:
        logging.error(f"Failed to write to Excel file: {e}")
        raise HTTPException(status_code=500, detail="Internal server error while writing to Excel file.")

def read_excel(create_if_not_exists: bool = True) -> pd.DataFrame:
    """Reads the Excel file or returns an empty DataFrame if the file does not exist. Optionally creates the file."""
    try:
        df = pd.read_excel(FILE_NAME)
    except FileNotFoundError:
        logging.info(f"{FILE_NAME} not found. Creating a new instance.")
        df = pd.DataFrame(columns=['name', 'quantity', 'price'])
        if create_if_not_exists:
            write_excel(df)
    return df

# Initialization step to ensure the Excel file exists at app start
read_excel()

@app.get("/items/", response_model=List[Item])
async def read_items():
    df = read_excel()
    return df.to_dict(orient="records")

@app.get("/items/{row_id}", response_model=Item)
async def read_item(row_id: int):
    df = read_excel()
    if row_id < 0 or row_id >= len(df):
        raise HTTPException(status_code=404, detail="Row not found")
    return df.iloc[row_id].to_dict()

@app.post("/items/", response_model=Item)
async def add_item(item: Item):
    df = read_excel()
    item_data = item.dict()
    df = pd.concat([df, pd.DataFrame([item_data])], ignore_index=True)
    write_excel(df)
    return item_data

@app.put("/items/{row_id}", response_model=Item)
async def update_item(row_id: int, item: Item):
    df = read_excel()
    if row_id < 0 or row_id >= len(df):
        raise HTTPException(status_code=404, detail="Row not found")
    # Update the row with item data
    for column in df.columns:
        if column in item.dict():
            df.at[row_id, column] = item.dict()[column]
    write_excel(df)
    return df.iloc[row_id].to_dict()

@app.delete("/items/{row_id}")
async def delete_item(row_id: int):
    df = read_excel()
    if row_id < 0 or row_id >= len(df):
        raise HTTPException(status_code=404, detail="Row not found")
    df = df.drop(index=row_id).reset_index(drop=True)
    write_excel(df)
    return {"message": "Item deleted successfully"}

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        with open(FILE_NAME, 'wb') as f:
            f.write(contents)
        logging.info("File uploaded successfully.")
        return {"message": "File uploaded successfully"}
    except Exception as e:
        logging.error(f"Failed to upload file: {e}")
        raise HTTPException(status_code=500, detail="Failed to upload file")
