def initAzure():
    import os
    
    os.makedirs('outputs', exist_ok=True)
    files = os.listdir("outputs")
    os.makedirs("outputs/_notebooks", exist_ok=True)
    os.makedirs("outputs/_models", exist_ok=True)
    os.makedirs("outputs/_metrics", exist_ok=True)
    os.makedirs("outputs/_datasets", exist_ok=True)
    
    if "_experiment-name_.txt" in files:
        
        with open("outputs/_experiment-name_.txt", "r", encoding = "utf-8") as file:
            name = file.readline()
            
        print(f"- There is an existing Experiment (name: '{name}') already in this working directory.")
        print("- All runs will be executed under this experiment name.")
        
    else:
        
        name = input("Enter the name of your Experiment (model-training) : ")
        with open("outputs/_experiment-name_.txt", "w", encoding = "utf-8") as file:
            file.write(name)

    print("Note the Name of your Experiment :", name, "\n")
    print("""=========== I M P O R T A N T ===========
    
    - Run the 'initAzure()' function just for one time in each Experiment (model-training) process.
    
    - You must work with your experiment (model-training) under a separate folder. 
      One folder, for each experiment.
      
    - All the log records (metrics, datasets, trained-model etc.) that you want to save should be 
      in the 'outputs' folder which is created in your working directory :
      - Data Sets should be saved into _'datasets' subfolder,
      - Metrics/log files should be saved into '_metrics' subfolder,
      - Trained models should be saved into '_models' subfolder,
      - A copy of Jupyter notebooks will be saved into '_notebooks' subfolder automatically.
      
    - All content of the 'outputs' folder will be uploaded to Azure cloud automatically when you 
      call 'toAzure()' function.
      
    - The size of uploading limit is upto 300 MB.
    
    - To upload the content of 'outputs' folder, call 'toAzure()' function when you finish 
      your training process (run). You should call 'toAzure()' function after each run (training).""")


def toAzure():
    import azureml.core
    from azureml.core import Workspace
    from azureml.core import Experiment
    import shutil, os, glob
    
    with open("outputs/_experiment-name_.txt", "r", encoding = "utf-8") as file:
        experiment_name = file.readline()
    
    ws = Workspace.get(name="jsl-workspace", 
                   subscription_id="e82292df-ef3b-4089-8f75-fcab8693c7ad",
                   resource_group='jsl-resources')
    
    experiment = Experiment(workspace=ws, name=experiment_name)
    
    notebooks = glob.glob("*.ipynb")
    for nb in notebooks:
        shutil.copy(nb, "outputs/_notebooks/CopyOf_"+nb)
    
    run = experiment.start_logging()
    print(f"Uploading the content of your '{experiment_name}' to Azure Cloud...")
    
    run.complete()
    runs = experiment.get_runs()
    
    print(f"Your {len(list(runs))}. run was uploaded.")
    print("""You can view your logs on Microsoft Azure Machine Learning Studio. To view the 
details of your last run, click the link below :""")
    
    runs = experiment.get_runs()
    return list(runs)[0]