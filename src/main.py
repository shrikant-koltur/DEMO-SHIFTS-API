import os
import uvicorn
from typing import List
from fastapi import FastAPI
import mysql.connector

app = FastAPI()

# Connect to MySQL

host = os.environ.get("DB_HOST")
user = os.environ.get("DB_USERNAME")
password = os.environ.get("DB_PASSWORD")
database = os.environ.get("DB_DATABASE")

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Geology@7",
    database="jod-test"
)
print("Connected to MySQL successfully!")

@app.get("/")
async def root():
    return {"message": "Hello World"}

# Fetch all shifts for a specific job
@app.get("/jobs/{job_id}/shifts", response_model=List[dict])
def get_shifts_for_job(job_id: int):

    """
    Fetch all slots for a specific shift.

    Args:
        shift_id (int): The ID of the shift.

    Returns:
        List[dict]: A list of slot dictionaries for the given shift ID.
    """

    cursor = db.cursor(dictionary=True)
    query = """
        SELECT s.*
        FROM shifts s
        JOIN jod_jobs j ON j.id = s.jod_job_id
        WHERE j.id = %s
    """
    cursor.execute(query, (job_id,))
    result = cursor.fetchall()
    cursor.close()
    return result

# Fetch all slots for a specific shift
@app.get("/shifts/{shift_id}/slots", response_model=List[dict])
def get_slots_for_shift(shift_id: int):
    """
    Fetch all users applied for a specific shift.

    Args:
        shift_id (int): The ID of the shift.

    Returns:
        List[dict]: A list of user dictionaries for the given shift ID.
    """

    cursor = db.cursor(dictionary=True)
    query = """
        SELECT sl.*
        FROM slots sl
        JOIN shifts s ON s.id = sl.shift_id
        WHERE s.id = %s
    """
    cursor.execute(query, (shift_id,))
    result = cursor.fetchall()
    cursor.close()
    return result

# Fetch all users applied for a specific shift
@app.get("/shifts/{shift_id}/users", response_model=List[dict])
def get_users_for_shift(shift_id: int):
    cursor = db.cursor(dictionary=True)
    query = """
        SELECT u.*
        FROM users u
        JOIN shift_user su ON su.app_user_id = u.id
        JOIN shifts s ON s.id = su.shift_id
        WHERE s.id = %s
    """
    cursor.execute(query, (shift_id,))
    result = cursor.fetchall()
    cursor.close()
    return result

# Fetch all slots and shifts for a specific job
@app.get("/jobs/{job_id}/slots-shifts", response_model=List[dict])
def get_slots_shifts_for_job(job_id: int):

    """
    Fetch all slots and shifts for a specific job.

    Args:
        job_id (int): The ID of the job.

    Returns:
        List[dict]: A list of slot dictionaries for the given job ID.
    """
    cursor = db.cursor(dictionary=True)
    query = """
        SELECT s.*
        FROM `slots` s
        JOIN `job_shift_mapping` jsm ON s.`shift_id` = jsm.`shift_id`
        JOIN `jod_jobs` j ON jsm.`job_id` = j.`id`
        WHERE j.`id` = %s
    """
    cursor.execute(query, (job_id,))
    result = cursor.fetchall()
    cursor.close()
    return result

# Fetch number of slots and shifts for a specific job
@app.get("/jobs/{job_id}/stats", response_model=dict)
def get_job_stats(job_id: int):
    """
    Fetch the number of slots and shifts for a specific job.

    Args:
        job_id (int): The ID of the job.

    Returns:
        dict: A dictionary containing the job ID, number of shifts, and number of slots.
    """
    cursor = db.cursor(dictionary=True)
    query = """
        SELECT
            j.id AS job_id,
            COUNT(DISTINCT jsm.shift_id) AS num_shifts,
            COUNT(s.id) AS num_slots
        FROM
            jod_jobs j
            LEFT JOIN job_shift_mapping jsm ON j.id = jsm.job_id
            LEFT JOIN slots s ON jsm.shift_id = s.shift_id
        WHERE
            j.id = %s
        GROUP BY
            j.id
    """
    cursor.execute(query, (job_id,))
    result = cursor.fetchone()
    cursor.close()
    if result:
        return result
    else:
        return {"error": "Job not found"}
    

# CREATE
# Add a new shift for a job
@app.post("/jobs/{job_id}/shifts", response_model=dict)
def create_shift(job_id: int, shift: dict):
    """
    Create a new shift for a specific job.

    Args:
        job_id (int): The ID of the job.
        shift (dict): The shift data to be created.

    Returns:
        dict: The created shift data.
    """
    cursor = db.cursor(dictionary=True)
    query = """
        INSERT INTO shifts (jod_job_id, hourly_rate, total_job_salary, x_available, shift_start_time, shift_end_time, shift_reminder, status, days_of_week, shift_template_id, created_at, updated_at, shift_uuid)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, NOW(), NOW(), %s)
    """
    values = (job_id, shift["hourly_rate"],shift["total_job_salary"],shift["x_available"],shift["shift_start_time"], shift["shift_end_time"], shift['shift_reminder'], shift['status'], shift['days_of_week'], shift['shift_template_id'], shift['shift_uuid'])
    cursor.execute(query, values)
    db.commit()
    shift_id = cursor.lastrowid  # Get the ID of the newly created shift

    # Update the job_shift_mapping table
    query = """
        INSERT INTO job_shift_mapping (job_id, shift_id, created_at, updated_at)
        VALUES (%s, %s, NOW(), NOW())
    """
    values = (job_id, shift_id)
    cursor.execute(query, values)
    db.commit()

    cursor.execute("SELECT * FROM shifts WHERE id = %s", (shift_id,))
    result = cursor.fetchone()
    cursor.close()
    return result

# UPDATE

# Update a shift
@app.put("/shifts/{shift_id}", response_model=dict)
def update_shift(shift_id: int, shift: dict):
    """
    Update an existing shift.

    Args:
        shift_id (int): The ID of the shift to be updated.
        shift (dict): The updated shift data.

    Returns:
        dict: The updated shift data.
    """
    cursor = db.cursor(dictionary=True)
    query = """
        UPDATE shifts
        SET hourly_rate = %s,
            total_job_salary = %s,
            x_available = %s,
            shift_start_time = %s,
            shift_end_time = %s,
            shift_reminder = %s,
            status = %s,
            days_of_week = %s,
            shift_template_id = %s,
            updated_at = NOW(),
            shift_uuid = %s
        WHERE id = %s
    """
    values = (
        shift["hourly_rate"],
        shift["total_job_salary"],
        shift["x_available"],
        shift["shift_start_time"],
        shift["shift_end_time"],
        shift["shift_reminder"],
        shift["status"],
        shift["days_of_week"],
        shift["shift_template_id"],
        shift["shift_uuid"],
        shift_id
    )
    cursor.execute(query, values)
    db.commit()
    cursor.execute("SELECT * FROM shifts WHERE id = %s", (shift_id,))
    result = cursor.fetchone()
    cursor.close()
    if result:
        return result
    else:
        return {"error": "Shift not found"}

# # DELETE
# # Delete a shift
# @app.delete("/shifts/{shift_id}", response_model=dict)
# def delete_shift(shift_id: int):
#     """
#     Delete an existing shift.

#     Args:
#         shift_id (int): The ID of the shift to be deleted.

#     Returns:
#         dict: A success or error message.
#     """
#     cursor = db.cursor()
#     query = """
#         DELETE FROM shifts WHERE id = %s
#     """
#     cursor.execute(query, (shift_id,))
#     rowcount = cursor.rowcount
#     db.commit()
#     cursor.close()
#     if rowcount > 0:
#         return {"message": "Shift deleted successfully"}
#     else:
#         return {"error": "Shift not found"}
    

# CREATE
# Add a new slot for a specific shift
@app.post("/shifts/{shift_id}/slots", response_model=dict)
def create_slot(shift_id: int, slot: dict):
    """
    Create a new slot for a specific shift.

    Args:
        shift_id (int): The ID of the shift.
        slot (dict): The slot data to be created.

    Returns:
        dict: The created slot data.
    """
    cursor = db.cursor(dictionary=True)
    query = """
        INSERT INTO slots (shift_id, slot_start_date, 
        slot_end_date, status, created_at, updated_at)
        VALUES (%s, %s, %s, %s, NOW(), NOW())
    """
    values = (shift_id, slot["slot_start_date"],
            slot["slot_end_date"], 
            slot["status"])
   
    cursor.execute(query, values)
    db.commit()
    slot_id = cursor.lastrowid
    cursor.execute("SELECT * FROM slots WHERE id = %s", (slot_id,))
    result = cursor.fetchone()
    cursor.close()
    return result

@app.put("/slots/{slot_id}", response_model=dict)
def update_slot(slot_id: int, slot: dict):
    """
    Update an existing slot.

    Args:
        slot_id (int): The ID of the slot to be updated.
        slot (dict): The updated slot data.

    Returns:
        dict: The updated slot data.
    """
    cursor = db.cursor(dictionary=True)
    query = """
        UPDATE slots
        SET shift_id = %s,
            slot_start_date = %s,
            slot_end_date = %s,
            status = %s,
            updated_at = NOW()
        WHERE id = %s
    """
    values = (
        slot["shift_id"],
        slot["slot_start_date"],
        slot["slot_end_date"],
        slot["status"],
        slot_id
    )
    cursor.execute(query, values)
    db.commit()
    cursor.execute("SELECT * FROM slots WHERE id = %s", (slot_id,))
    result = cursor.fetchone()
    cursor.close()
    if result:
        return result
    else:
        return {"error": "Slot not found"}

# DELETE
# Delete a shift
@app.delete("/shifts/{shift_id}", response_model=dict)
def delete_shift(shift_id: int):
    """
    Delete an existing shift.

    Args:
        shift_id (int): The ID of the shift to be deleted.

    Returns:
        dict: A success or error message.
    """
    cursor = db.cursor()
    query = """
        DELETE FROM shifts WHERE id = %s
    """
    cursor.execute(query, (shift_id,))
    rowcount = cursor.rowcount
    db.commit()
    cursor.close()
    if rowcount > 0:
        return {"message": "Shift deleted successfully"}
    else:
        return {"error": "Shift not found"}
    
# DELETE
# Delete a slot
@app.delete("/slots/{slot_id}", response_model=dict)
def delete_slot(slot_id: int):
    """
    Delete an existing slot.

    Args:
        slot_id (int): The ID of the slot to be deleted.

    Returns:
        dict: A success or error message.
    """
    cursor = db.cursor()
    query = """
        DELETE FROM slots WHERE id = %s
    """
    cursor.execute(query, (slot_id,))
    rowcount = cursor.rowcount
    db.commit()
    cursor.close()
    if rowcount > 0:
        return {"message": "Slot deleted successfully"}
    else:
        return {"error": "Slot not found"}
    




if __name__ == '__main__':
    uvicorn.run(app, port=7000, host='0.0.0.0')