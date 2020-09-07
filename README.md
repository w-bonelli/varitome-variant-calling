# Snakemato

**Alignment and variant calling pipeline for the [Varitome](https://solgenomics.net/projects/varitome) project.**

This pipeline is composed with [Snakemake](https://snakemake.readthedocs.io/en/stable/index.html) v5.23.0. Compatibility with different versions is not guaranteed

## Installation

Clone this repository with `git clone https://github.com/van-der-knaap-lab/snakemato.git`. On GACRC's Sapelo2, you will need to load the Git module first with  `ml load git/2.23.0-GCCcore-8.3.0-nodocs`.

## Configuration

On GACRC's Sapelo2, this pipeline must run in the scratch filesystem (`/scratch/<user>`), otherwise filesystem quotas will quickly be exceeded.

The pipeline is defined in `Snakefile`. It accepts a config file (e.g., `config.json`) which must be located in the same directory. The config file should conform to the following schema:

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

Note that the reference genome file (`something.fasta`) must exist in the same directory.

## Usage

To execute a dry run prior (does not actually do anything, just prints out rules scheduled for execution), you first need a conda environment with Snakemake v5.23 installed. To create one on Sapelo2:

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

Execute the dry run with:

```bash
snakemake -np --config-file "<config file>"
```

You probably won't want to run the pipeline interactively unless your dataset is very small and you have a `tmux` or `screen` session open, as the pipeline will take several hours at minimum &mdash; but if you do, run:

```bash
snakemake --latency-wait 30 --restart-times 2 --configfile "<config file>" --jobs 500 --cluster "qsub -l walltime={params.walltime} -l nodes={params.nodes}:ppn={params.ppn} -l mem={params.mem} -M <your email address> -m ae"
```

Several command line arguments are passed to Snakemake:

- `--latency-wait`: seconds to wait after each rule completes before checking for expected output files (compensates for filesystem latency)
- `--restart-times`: times to restart each rule if it fails
- `--jobs`: maximum number of concurrent jobs submitted to the cluster scheduler
- `--cluster`: the command to use when submitting each job to the cluster scheduler; parameters (e.g., `params.walltime`) are specified in `Snakefile` on a per-rule basis

These options can be reconfigured as needed.

To submit the pipeline to Sapelo2 as a batch job, simply embed the command above in a job submission script (several examples follow).

### Torque/Moab (PBS)

```
#PBS -S /bin/bash
#PBS -N Snakemato
#PBS -q batch
#PBS -l nodes=1:ppn=1
#PBS -l walltime=150:00:00
#PBS -l mem=20gb
#PBS -M <your email address>
#PBS -m ae

cd $PBS_O_WORKDIR

module load Miniconda3/4.7.10
source activate alignment

ulimit -c unlimited

snakemake --latency-wait 30 --restart-times 2 --configfile "config.json" --jobs 500 --cluster "qsub -l walltime={params.walltime} -l nodes={params.nodes}:ppn={params.ppn} -l mem={params.mem} -M <your email address> -m ae"
```

### Slurm

```
TODO
```
