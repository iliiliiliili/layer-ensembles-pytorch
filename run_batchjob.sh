#!/bin/bash 
#SBATCH -J vnn 
#SBATCH -o ./batchjob/vnn_%a.o 
#SBATCH -e ./batchjob/vnn_%a.e 
#SBATCH --account=zhangh 
#SBATCH --mem=16G 
#SBATCH --cpus-per-task=8
#SBATCH --ntasks=1 
#SBATCH -p gpu 
#SBATCH -t 1-00:00:00 
#SBATCH --gres=gpu:v100:1
#SBATCH --array=0-1 
module purge 
module load pytorch/1.11
srun python3 modeling.py run_indexed --index=$SLURM_ARRAY_TASK_ID --output-dir="./models/"
