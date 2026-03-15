import os
from pathlib import Path # Automatic adjust (/ or \) depend on the os system: window(/), Mac(\)

project_name = "us_visa"

# f-string: insert value of the variable in the {}

list_of_files = [
    f"{project_name}/__init__.py" # Constructor file, it define that this folder is local package
    f"{project_name}/components" # Main step
    f"{project_name}/components/data_ingestion.py",  
    f"{project_name}/components/data_validation.py",
    f"{project_name}/components/data_transformation.py",
    f"{project_name}/components/model_trainer.py",
    f"{project_name}/components/model_evaluation.py",
    f"{project_name}/components/model_pusher.py",
    f"{project_name}/configuration/__init__.py",
    f"{project_name}/constants/__init__.py", # Store path, parameters
    f"{project_name}/entity/__init__.py", # Define structure of input/output 
    f"{project_name}/entity/config_entity.py",
    f"{project_name}/entity/artifact_entity.py",
    f"{project_name}/exception/__init__.py",
    f"{project_name}/logger/__init__.py",
    f"{project_name}/pipline/__init__.py", # Connect components to become a full pipeline
    f"{project_name}/pipline/training_pipeline.py",
    f"{project_name}/pipline/prediction_pipeline.py",
    f"{project_name}/utils/__init__.py", # "Hàm bổ trợ" (Read yaml file, save model)
    f"{project_name}/utils/main_utils.py",
    "app.py",
    "requirements.txt",
    "Dockerfile",
    ".dockerignore",
    "demo.py",
    "setup.py",
    "config/model.yaml",
    "config/schema.yaml",
]

for filepath in list_of_files:
    filepath = Path(filepath) # Convert the string into Path Object
    filedir, filename = os.path.split(filepath) # Split the path into the folder and file path
    if (filedir != ""):
        os.makedirs(filedir, exist_ok=True) # Create new folder, exist_ok=True if folder is exist then pass without Error
    if (not os.path.exists(filepath) or (os.path.getsize(filepath))): # If file is not exist or file is empty
        with open(filepath, "w") as f: # Open file in "write" mode
            pass # Do nothing, just open and close to create file
    else:
        print(f"file is already present at: {filepath}")

