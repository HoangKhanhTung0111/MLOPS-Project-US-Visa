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

## Library conflict solution 
1. Use install (Conda automatic remove and reinstall)
```bash
conda install ten_thu_vien=phien_ban_moi --freeze-installed
# VD: conda install pandas=1.5.3
```
2. Use update
```bash
conda update ten_thu_vien
```
3. Use remove
```bash
conda remove ten_thu_vien
conda install ten_thu_vien=phien_ban_dung
```
4. Remove conda
```bash
conda deactivate
conda remove -n myenv --all
# And then run like "How to run" section
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