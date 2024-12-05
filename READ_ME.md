Dependencies: Numpy, math, sqlite3(if one wants to use already compiled models), Matplotlib

In /Users/johanneswalka/Documents/Documents/Implementierung_Bachelorarbeit/Models/Compiled_Models/SC_compiled.db you can fined already compiled Models from the Spacial Clustered Modul in a SQL table. 






## ML-Cloud

#!/bin/bash

#SBATCH --job-name=name           # Job name
#SBATCH --ntasks=1                # Number of tasks
#SBATCH --nodes=1                 # Ensure that all cores are on one machine
#SBATCH --time=1-00:00            # Runtime in D-HH:MM - takes about an hour per epoch on 2 GPUs
#SBATCH --partition=2080-galvani  # Partition to submit to
#SBATCH --mem=40G                 # Memory pool for all cores
#SBATCH --gres=gpu:0              # Request one GPU
#SBATCH --cpus-per-task=8        # Request all 8 CPUs per GPU
#SBATCH --mail-user=o@walka.de  # Email address for notifications
#SBATCH --mail-type=BEGIN,END,FAIL  # When to send email notifications
# include information about the job in the output
scontrol show job=$SLURM_JOB_ID

# run the actual command
srun \
singularity exec \
--nv \
/mnt/qb/work/wichmann/wzz745/ffcv.sif \
./train.sh

# da um so ein 
--bind /mnt/lustre/datasets/ \
--bind /mnt/qb/work/wichmann/wzz745 \
--bind /scratch_local/ \

# train.sh da wird im Prinzip dann alles ausgeführt 
python3 ./save-images-from-activations.py <——— das steht da einfach drin


# Das führt man einmal aus nachdem die File erstellt wurde skript zum starten eines jobs
chmod +x filename.sh

# sbatch um Skript auszuführen
sbatch script.sh
# squeue um zu schauen wie die jobs laufen 
squeue -u lfz080
# job löschen
scancel JOBID


Script.sh und tests.py schicken und fragen das er einen Kontainer bauen soll

Script.sh und train.sh sind die beiden Dateien die dann letzten Endes ausgeführt werden müssen. Nein. In Script.sh muss unten hin train.sh was es schon ist. Man muss dann also nur noch script.sh ausführen.


Bootstrap: docker
From: python:3.9-slim

%post
    # Installiere die notwendigen Python-Pakete
    pip install --no-cache-dir matplotlib numpy scipy math pickle 

%files
    # Keine Notwendigkeit, die Projektdateien in das Image zu kopieren, da sie extern gebunden werden
    # . /app

%environment
    # Setze Umgebungsvariablen, falls nötig
    # export PATH=/usr/local/bin:$PATH

%runscript
    # Placeholder, falls der Container direkt ausgeführt wird. Da srun/singularity exec genutzt wird, ist dies unnötig.
    # echo "Singularity container for executing train.sh"




