# Varitome Variant Calling

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [Installation](#installation)
- [Prerequisites](#prerequisites)
- [Pipelines](#pipelines)
  - [Variant Calling](#variant-calling)
    - [Configuration](#configuration)
    - [Usage](#usage)
      - [Torque/Moab (PBS)](#torquemoab-pbs)
      - [Slurm](#slurm)
  - [Read Depths](#read-depths)
    - [Configuration](#configuration-1)
    - [Usage](#usage-1)
      - [Torque/MOAB](#torquemoab)
- [Utils](#utils)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

Pipelines in this repository are composed with [Snakemake](https://snakemake.readthedocs.io/en/stable/index.html) v5.23.0. Compatibility with different versions is not guaranteed.

## Installation

Clone this repository with `git clone https://github.com/van-der-knaap-lab/snakemato.git`. On GACRC's Sapelo2, you will need to load the Git module first with  `ml load git/2.23.0-GCCcore-8.3.0-nodocs`.

## Prerequisites

You will first need a conda environment with Snakemake installed. To create one on Sapelo2:

```bash
module load Miniconda3/4.7.10
conda create --name <myenv>
source activate <myenv>
conda install -c conda-forge -c bioconda snakemake
```

If an appropriate conda environment already exists, just run:

```bash
module load Miniconda3/4.7.10
source activate <myenv>
```

## Pipelines

### Variant Calling

The `Snakefile.variants` pipeline involves the following steps:

- download fastq files
- merge fastq files for each accession
- trim fastq files with Trimmomatic
- align reads with a reference genome with SpeedSeq
- sort the aligned sequence with SAMtools
- create read groups with Picard
- mark duplicates with Picard
- call variants with LUMPY
- call variants with GATK HaplotypeCaller
- combine variants returned from HaplotypeCaller
- joint genotype then select and filter variants with GATK

#### Configuration

On GACRC's Sapelo2, pipelines must run in the scratch filesystem (`/scratch/<user>`), otherwise filesystem quotas will quickly be exceeded.

This pipeline accepts a config file (e.g., `config.json`) which must be located in the same directory. The config file should conform to the following schema:

```json
{
  "reference": "<reference genome>",
  "accessions": {
    "<accession 1>": [
      "<run 1>",
      "<run 2>"
    ],
    "<accession 2>": [
      "<run 1>",
      "<run 2>"
    ]
  }
}
```

For instance, to run 2 accessions (each with a variable number of sequencer runs) against the "PAS014479_MAS1.0" reference genome:

```json
{
  "reference": "PAS014479_MAS1.0",
  "accessions": {
    "BGV012640": [
      "SRR7279605"
    ],
    "PI487625": [
      "SRR7279526",
      "SRR7279658"
    ]
  }
}
```

Note that the reference genome file (e.g., `PAS014479_MAS1.0.fasta`) must exist in the same directory.

#### Usage

To execute a dry run (does not actually do anything, just prints out rules scheduled for execution):

```bash
snakemake --snakefile Snakefile.variants -np --configfile "<config file>"
```

You probably won't want to run the pipeline interactively unless your dataset is very small and you have a [tmux](https://github.com/tmux/tmux) or [screen](https://www.gnu.org/software/screen/) session open, as the pipeline will take several hours at minimum &mdash; but if you do, run:

```bash
snakemake --snakefile Snakefile.variants --latency-wait 30 --restart-times 2 --configfile "<config file>" --jobs 500 --cluster "qsub -l walltime={params.walltime} -l nodes={params.nodes}:ppn={params.ppn} -l mem={params.mem} -M <your email address> -m ae"
```

Several command line arguments are passed to Snakemake:

- `--latency-wait`: seconds to wait after each rule completes before checking for expected output files (compensates for filesystem latency)
- `--restart-times`: times to restart each rule if it fails
- `--jobs`: maximum number of concurrent jobs submitted to the cluster scheduler
- `--cluster`: the command to use when submitting each job to the cluster scheduler; parameters (e.g., `params.walltime`) are specified in `Snakefile` on a per-rule basis

These options can be reconfigured as needed. Note that if the pipeline has run previously in the same directory, you may need to execute a dry run with extra flag `--unlock` to release the directory lock before rerunning. Alternatively use `--nolock` to ignore directory locks.

To submit the pipeline to Sapelo2 as a batch job, simply embed the command above in a job submission script (several examples follow).

##### Sample Job Scripts

Depending on the size of your dataset you may need to tune cluster resources on a per-rule basis. If your dataset is large, you may need to either use your cluster's high-memory queue or split the dataset into chunks (`combine_variants` and subsequent rules are memory-hungry, since they operate on all variants at once).

**Torque/Moab (PBS)**

```
#PBS -S /bin/bash
#PBS -N varitome-variants
#PBS -q batch
#PBS -l nodes=1:ppn=1
#PBS -l walltime=150:00:00
#PBS -l mem=20gb
#PBS -M <your email address>
#PBS -m ae

cd $PBS_O_WORKDIR

module load Miniconda3/4.7.10
source activate <your conda environment>

ulimit -c unlimited

snakemake --snakefile Snakefile.variants  --latency-wait 30 --restart-times 2 --configfile "config.json" --jobs 500 --cluster "qsub -l walltime={params.walltime} -l nodes={params.nodes}:ppn={params.ppn} -l mem={params.mem} -M <your email address> -m ae"
```

**Slurm**

```
#!/bin/bash
#SBATCH --job-name=varitome-variants
#SBATCH --partition=batch
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=20gb
#SBATCH --time=168:00:00
#SBATCH --mail-type==END,FAIL
#SBATCH --mail-user=<your email address>
#SBATCH --output=varitome.variants.%j.out
#SBATCH --error=varitome.variants.%j.err

cd $SLURM_SUBMIT_DIR

module load Anaconda3/2020.02
source activate alignment

ulimit -c unlimited

snakemake --latency-wait 30 --restart-times 2 --configfile "config.json" --jobs 500 --cluster "sbatch --time={params.walltime} --ntasks={params.nodes} --cpus-per-task={params.ppn} --mem={params.mem} --mail-type=END,FAIL --mail-user=<your email address>"
```

### Read Depths

The `Snakefile.depths` pipeline calculates average read depths for a collection of `.bam` files. 
 
#### Configuration

This pipeline accepts a configuration file with schema:

```json
{
  "accessions":  [
      "<accession 1>",
      "<accession 2>"
  ]
}
```

The pipeline expects `.bam` files in the working directory. Files should be named `<accession>.bam`.

#### Usage

To execute a dry run (does not actually do anything, just prints out rules scheduled for execution):

```bash
snakemake --snakefile Snakefile.depths -np --configfile "<config file>"
```

To execute the pipeline interactively (this should be done from an interactive job):

```bash
snakemake --snakefile Snakefile.depths --latency-wait 30 --restart-times 2 --configfile "<config file>" --jobs 500 --cluster "qsub -l walltime={params.walltime} -l nodes={params.nodes}:ppn={params.ppn} -l mem={params.mem} -M <your email address> -m ae"
```

Several command line arguments are passed to Snakemake:

- `--latency-wait`: seconds to wait after each rule completes before checking for expected output files (compensates for filesystem latency)
- `--restart-times`: times to restart each rule if it fails
- `--jobs`: maximum number of concurrent jobs submitted to the cluster scheduler
- `--cluster`: the command to use when submitting each job to the cluster scheduler; parameters (e.g., `params.walltime`) are specified in `Snakefile` on a per-rule basis

These options can be reconfigured as needed. Note that if the pipeline has run previously in the same directory, you may need to execute a dry run with extra flag `--unlock` to release the directory lock before rerunning. Alternatively use `--nolock` to ignore directory locks.

##### Sample Job Scripts

**Torque/MOAB**

```bash
#PBS -S /bin/bash
#PBS -N varitome-depths
#PBS -q batch
#PBS -l nodes=1:ppn=1
#PBS -l walltime=24:00:00
#PBS -l mem=20gb
#PBS -M <your email address>
#PBS -m ae

cd $PBS_O_WORKDIR

module load Miniconda3/4.7.10
source activate <your conda environment>

ulimit -c unlimited

snakemake --snakefile Snakefile.depths --configfile depths_config.json --latency-wait 30 --restart-times 2 --jobs 500 --cluster "qsub -l walltime={params.walltime} -l nodes={params.nodes}:ppn={params.ppn} -l mem={params.mem} -M <your email address> -m ae"
```

**Slurm**

```
#!/bin/bash
#SBATCH --job-name=varitome-depths
#SBATCH --partition=batch
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=20gb
#SBATCH --time=168:00:00
#SBATCH --mail-type==END,FAIL
#SBATCH --mail-user=<your email address>
#SBATCH --output=varitome.depths.%j.out
#SBATCH --error=varitome.depths.%j.err

cd $SLURM_SUBMIT_DIR

module load Anaconda3/2020.02
source activate alignment

ulimit -c unlimited

"snakemake --snakefile Snakefile.depths --configfile depths_config.json --latency-wait 30 --restart-times 2 --jobs 500 --cluster "qsub -l walltime={params.walltime} -l nodes={params.nodes}:ppn={params.ppn} -l mem={params.mem} -M <your email address> -m ae"
```

## Utils

Various utilities carried over from previous collaborator Nathan.
