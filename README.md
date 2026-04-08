# MLOPS-Project-US-Visa

- Anaconda: https://www.anaconda.com/
- VS Code: https://code.visualstudio.com/download
- Git: https://git-scm.com/install/
- Flowchart: https://whimsical.com/
- MLOPS tools: https://www.evidentlyai.com/
- MongoDB: https://account.mongodb.com/account/login
- Data Link: https://www.kaggle.com/datasets/moro23/easyvisa-dataset?resource=download

## Git Commands
```bash
git add .

git commit -m "Update"

git push origin main
```

## How to run?
```bash
conda create -n visa python=3.10 -y
```

```bash
conda activate visa
```

```bash
pip install -r requirements.txt
```

## Workflow (order to update files):

1. constants
2. entity
3. components
4. pipeline
5. Main file

## Export the environment variable (use for gitbash, linux,...)
```bash
export MONGODB_URL="mongodb+srv://<username>:<password>...."
```