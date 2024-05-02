# SHIFTS and SLOTS APIS in FastAPI

To install Python on your system, you can follow these steps:

### macOS:

1. **Homebrew (recommended):**

   - Open Terminal.
   - Install Homebrew if you haven't already:

     ```bash
     /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
     ```

   - Install Python using Homebrew:

     ```bash
     brew install python
     ```

2. **Using macOS Installer:**
   - Download the latest Python installer from the [official Python website](https://www.python.org/downloads/mac-osx/).
   - Double-click the downloaded `.pkg` file and follow the instructions to install Python.

### Windows:

1. **Official Python Installer:**
   - Download the latest Python installer from the [official Python website](https://www.python.org/downloads/windows/).
   - Run the downloaded `.exe` file.
   - Make sure to check the box that says "Add Python to PATH" during installation.
   - Follow the installation instructions.

### Verify Installation:

After installing Python, you can verify the installation by opening Command Prompt (Windows) or Terminal (macOS) and running the following commands:

- Check Python version:

  ```bash
  python --version
  ```

- Check pip version (Python package manager):

  ```bash
  pip --version
  ```

---

## Follow below steps to create Virtual Environment to run the python backend

## macOS:

#### Create Virtual Environment:

1. Open Terminal.
2. Navigate to your project directory.
3. Run the following command to create a virtual environment named `venv`:

   ```bash
   python3 -m venv venv
   ```

4. Activate the virtual environment:

   ```bash
   source venv/bin/activate
   ```

#### Install Dependencies:

1. With the virtual environment activated, install your project dependencies using `pip`:

   ```bash
   pip install -r requirements.txt
   ```

### Windows:

#### Create Virtual Environment:

1. Open Command Prompt.
2. Navigate to your project directory.
3. Run the following command to create a virtual environment named `venv`:

   ```bash
   python -m venv venv
   ```

4. Activate the virtual environment:

   ```bash
   venv\Scripts\activate
   ```

#### Install Dependencies:

1. With the virtual environment activated, install your project dependencies using `pip`:

   ```bash
   pip install -r requirements.txt
   ```

# Project Name

SHIFTS and SLOTS APIS in FastAPI

## Installation

1. Clone the repository:

   ```bash
   git clone <repository_url>
   ```

2. Navigate to the project directory:

   ```bash
   cd src
   ```

3. Create a virtual environment:

   ```bash
   # macOS
   python3 -m venv venv

   # Windows
   python -m venv venv
   ```

4. Activate the virtual environment:

   ```bash
   # macOS
   source venv/bin/activate

   # Windows
   venv\Scripts\activate
   ```

5. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

6. Run the server

```bash
uvicorn src.main:app --port 7000 --reload
```

7. Swagger UI - Alternative of postman where you can put payload and check the APIs

Go to `http://127.0.0.1:7000/docs`

---

# APIS

## For `GET` functions just add required IDs and run it.

### POST `/jobs/{job_id}/shifts`

## Create Shift

- Create a new shift for a specific job.
- Args: job_id (int): The ID of the job.
- shift (dict): The shift data to be created.
- Returns: dict: The created shift data.

```bash
{
    "hourly_rate": 34,
    "total_job_salary": 578,
    "x_available": true,
    "shift_start_time": "2024-04-26 08:00:00",
    "shift_end_time": "24-04-26 18:00:00",
    "shift_reminder": 2,
    "status": 1,
    "days_of_week": "Sunday",
    "shift_template_id": 1,
    "shift_uuid": "83u4egjfbh"
}
```

### POST `/shifts/{shift_id}/slots`

## Create Slot

- Create a new slot for a specific shift.
- Args: shift_id (int): The ID of the shift.
- slot (dict): The slot data to be created.
- Returns: dict: The created slot data.

```bash
{
    "slot_start_date": "2024-04-26 08:00:00",
    "slot_end_date": "24-04-26 18:00:00",
    "status": 1
}
```

### PUT `/shifts/{shift_id}`

## Update Shift

Update an existing shift.

- Args: shift_id (int): The ID of the shift to be updated.
- shift (dict): The updated shift data.
- Returns: dict: The updated shift data.

```bash
{
    "hourly_rate": 25.5,
    "total_job_salary": 1000.0,
    "x_available": 5,
    "shift_start_time": "2024-04-29 08:00:00",
    "shift_end_time": "2024-04-29 18:00:00",
    "shift_reminder": 30,
    "status": 1,
    "days_of_week": "Monday",
    "shift_template_id": 2,
    "shift_uuid": "c9b9e8f7d2e5f3c4e7c2"
}
```

### PUT `/slots/{slot_id}`

## Update Slot

- Update an existing slot.
- Args: slot_id (int): The ID of the slot to be updated.
- slot (dict): The updated slot data.
- Returns: dict: The updated slot data.

```bash
{
    "shift_id":5,
    "slot_start_date": "2023-05-01 08:00:00",
    "slot_end_date": "2023-05-05 18:00:00",
    "status": 3
}
```
