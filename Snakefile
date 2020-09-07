accession_regex = "[a-zA-Z0-9_]+"

from copy import deepcopy

def flatten(nested_list):
	nested_list = deepcopy(nested_list)
	while nested_list:
		sublist = nested_list.pop(0)
		if isinstance(sublist, list):
			nested_list = sublist + nested_list
		else:
			yield sublist

run_fastqs = list(flatten([[f"{run}_1.fastq", f"{run}_2.fastq"] for runs in config["accessions"].values() for run in runs]))
accession_fastqs = list(flatten([[f"{accession}_1.fastq", f"{accession}_2.fastq"] for accession in config["accessions"].keys()]))

rule all:
	input: ["combined.genotyped.selected.filtered.recoded.vcf"] + [f"{accession}.lumpy.vcf" for accession in config["accessions"]]

rule dump_fastqs:
	output: run_fastqs + [touch("dump_fastqs.done")]
	threads: 10
	run:
		for runs in config["accessions"].values():
			for run in runs:
				shell("module load Miniconda3/4.7.10 && source activate alignment && ulimit -c unlimited && parallel-fastq-dump --split-files -t {threads} -s {run}")

rule merge_fastqs:
	input: "dump_fastqs.done"
	output: accession_fastqs + [touch("merge_accessions.done")]
	params:
		walltime="12:00:00",
		nodes=1,
		ppn=1,
		mem="40gb"
	run:
		for accession, runs in config["accessions"].items():
			shell("cat " + " ".join([f"{run}_1.fastq " for run in runs]) + f"> {accession}_1.fastq")
			shell("cat " + " ".join([f"{run}_2.fastq " for run in runs]) + f"> {accession}_2.fastq")

rule trim_fastqs:
	input:
		flag="merge_accessions.done",
		one="{accession}_1.fastq",
		two="{accession}_2.fastq"
	output:
		one="{accession}_1.trimmed.fastq",
		two="{accession}_2.trimmed.fastq",
		one_unpaired="{accession}_1.unpaired.trimmed.fastq",
		two_unpaired="{accession}_2.unpaired.trimmed.fastq"
	wildcard_constraints:
		accession=accession_regex
	threads: 20
	params:
		walltime="04:00:00",
		nodes=1,
		ppn=20,
		mem="40gb"
	shell:
		"""
		module load Trimmomatic/0.36-Java-1.8.0_144
		ulimit -c unlimited
		time java -jar /usr/local/apps/eb/Trimmomatic/0.36-Java-1.8.0_144/trimmomatic-0.36.jar PE -threads {threads} {input.one} {input.two} {output.one} {output.one_unpaired} {output.two} {output.two_unpaired} SLIDINGWINDOW:4:20 MINLEN:20
		"""

rule align:
	input:
		one="{accession}_1.trimmed.fastq",
		two="{accession}_2.trimmed.fastq",
	output:
		bam="align_{accession}/{accession}.bam",
		splitters="align_{accession}/{accession}.splitters.bam",
		discordants="align_{accession}/{accession}.discordants.bam"
	wildcard_constraints:
		accession=accession_regex
	threads: 20
	params:
		reference=f"{config['reference']}.fasta",
		readgroup=lambda wildcards: r"@RG\tID:" + wildcards.accession + r"\tSM:" + wildcards.accession + r"\tLB:" + wildcards.accession,
		walltime="16:00:00",
		nodes=1,
		ppn=20,
		mem="100gb"
	shell:
		"""
		module load SpeedSeq/0.1.2-foss-2016b
		ulimit -c unlimited
		one=$(readlink -f {input.one})
		two=$(readlink -f {input.two})
		mkdir -p align_{wildcards.accession}
		cp {params.reference} align_{wildcards.accession}/{params.reference}
		cd align_{wildcards.accession}
		speedseq align -M 60 -t {threads} -i -R '{params.readgroup}' -o '{wildcards.accession}' {params.reference} $one $two
		"""

rule detect_breakpoints:
	input:
		bam="align_{accession}/{accession}.bam",
		splitters="align_{accession}/{accession}.splitters.bam",
		discordants="align_{accession}/{accession}.discordants.bam"
	wildcard_constraints:
		accession=accession_regex
	output:
		"{accession}.lumpy.vcf"
	params:
		walltime="10:00:00",
		nodes=1,
		ppn=20,
		mem="58gb"
	shell:
		"""
		module load LUMPY/0.2.13-foss-2016b
		ulimit -c unlimited
		lumpyexpress -B {input.bam} -S {input.splitters} -D {input.discordants} -o {output}
		"""

rule sort:
	input:
		"align_{accession}/{accession}.bam"
	output:
		"{accession}.sorted.bam"
	wildcard_constraints:
		accession=accession_regex
	params:
		walltime="12:00:00",
		nodes=1,
		ppn=1,
		mem="58gb"
	shell:
		"""
		module load SAMtools/1.9-foss-2016b
		ulimit -c unlimited
		samtools sort -m 25G {input} -o {output}
		"""

rule create_read_groups:
	input:
		"{accession}.sorted.bam"
	output:
		"{accession}.sorted.grouped.bam"
	wildcard_constraints:
		accession=accession_regex
	params:
		walltime="05:00:00",
		nodes=1,
		ppn=1,
		mem="20gb"
	shell:
		"""
		module load picard/2.16.0-Java-1.8.0_144
		ulimit -c unlimited
		java -classpath /usr/local/apps/eb/picard/2.16.0-Java-1.8.0_144 -jar /usr/local/apps/eb/picard/2.16.0-Java-1.8.0_144/picard.jar AddOrReplaceReadGroups INPUT={input} OUTPUT={output} RGID={wildcards.accession} RGSM={wildcards.accession} RGLB={wildcards.accession} RGPL=ILLUMINA RGPU=ignore
		"""

rule mark_duplicates_and_build_index:
	input:
		"{accession}.sorted.grouped.bam"
	output:
		bam="{accession}.sorted.grouped.marked.bam",
		met="{accession}.sorted.grouped.marked.metrics.txt"
	wildcard_constraints:
		accession=accession_regex
	params:
		walltime="12:00:00",
		nodes=1,
		ppn=1,
		mem="40gb"
	shell:
		"""
		module load picard/2.16.0-Java-1.8.0_144
		ulimit -c unlimited
		java -classpath /usr/local/apps/eb/picard/2.16.0-Java-1.8.0_144 -jar /usr/local/apps/eb/picard/2.16.0-Java-1.8.0_144/picard.jar MarkDuplicates INPUT={input} OUTPUT={output.bam} METRICS_FILE={output.met}
		java -classpath /usr/local/apps/eb/picard/2.16.0-Java-1.8.0_144 -jar /usr/local/apps/eb/picard/2.16.0-Java-1.8.0_144/picard.jar BuildBamIndex INPUT={output.bam}
		"""

rule create_reference_index:
	output: f"{config['reference']}.fasta.fai"
	params:
		reference=f"{config['reference']}.fasta",
		walltime="05:00:00",
		nodes=1,
		ppn=1,
		mem="20gb"
	shell:
		"""
		module load SAMtools/1.9-foss-2016b
		ulimit -c unlimited
		samtools faidx {params.reference}
		"""

rule create_reference_sequence_dictionary:
	output: f"{config['reference']}.dict"
	params:
		reference=f"{config['reference']}.fasta",
		walltime="05:00:00",
		nodes=1,
		ppn=1,
		mem="20gb"
	shell:
		"""
		module load GATK/4.1.6.0-GCCcore-8.2.0-Java-1.8
		ulimit -c unlimited
		gatk CreateSequenceDictionary -R {params.reference}
		"""

rule call_variants:
	input:
		index=f"{config['reference']}.fasta.fai",
		dict=f"{config['reference']}.dict",
		bam="{accession}.sorted.grouped.marked.bam"
	output:
		"{accession}.variants.vcf"
	wildcard_constraints:
		accession=accession_regex
	threads: 20
	params:
		reference=f"{config['reference']}.fasta",
		walltime="24:00:00",
		nodes=1,
		ppn=20,
		mem="58gb"
	shell:
		"""
		module load GATK/4.1.6.0-GCCcore-8.2.0-Java-1.8
		ulimit -c unlimited
		gatk HaplotypeCaller --native-pair-hmm-threads {threads} -R {params.reference} -I {input.bam} -ERC GVCF -O {output}
		"""

rule combine_variants:
	input:
		expand("{accession}.variants.vcf", accession=config["accessions"].keys())
	output:
		"combined.vcf"
	params:
		reference=f"{config['reference']}.fasta",
		variants=lambda wildcards, input: " ".join([f"-V {variant}" for variant in input]),
		walltime="48:00:00",
		nodes=1,
		ppn=1,
		mem="58gb"
	shell:
		"""
		module load GATK/4.1.6.0-GCCcore-8.2.0-Java-1.8
		ulimit -c unlimited
		gatk CombineGVCFs -R {params.reference} {params.variants} -O {output}
		"""

rule joint_genotype:
	input:
		"combined.vcf"
	output:
		"combined.genotyped.vcf"
	params:
		reference=f"{config['reference']}.fasta",
		walltime="48:00:00",
		nodes=1,
		ppn=1,
		mem="58gb"
	shell:
		"""
		module load GATK/4.1.6.0-GCCcore-8.2.0-Java-1.8
		ulimit -c unlimited
		gatk GenotypeGVCFs -R {params.reference} -V {input} -O {output}
		"""

rule select_variants:
	input:
		"combined.genotyped.vcf"
	output:
		"combined.genotyped.selected.vcf"
	params:
		reference=f"{config['reference']}.fasta",
		walltime="48:00:00",
		nodes=1,
		ppn=1,
		mem="58gb"
	shell:
		"""
		module load GATK/4.1.6.0-GCCcore-8.2.0-Java-1.8
		ulimit -c unlimited
		gatk SelectVariants -R {params.reference} -V {input} --select-type-to-include SNP -O {output}
		"""

rule filter_variants:
	input:
		"combined.genotyped.selected.vcf"
	output:
		"combined.genotyped.selected.filtered.vcf"
	params:
		reference=f"{config['reference']}.fasta",
		walltime="48:00:00",
		nodes=1,
		ppn=1,
		mem="58gb"
	shell:
		"""
		module load GATK/4.1.6.0-GCCcore-8.2.0-Java-1.8
		ulimit -c unlimited
		gatk VariantFiltration -R {params.reference} -V {input} -O {output} --filter-name 'Default_recommended' --filter-expression 'QD < 2.0 || FS > 60.0 || MQ < 40.0 || MQRankSum  < -12.5 || ReadPosRankSum < -8.0' -O
		"""

rule recode_variants:
	input:
		"combined.genotyped.selected.filtered.vcf"
	output:
		"combined.genotyped.selected.filtered.recoded.vcf"
	params:
		reference=f"{config['reference']}.fasta",
		walltime="48:00:00",
		nodes=1,
		ppn=1,
		mem="58gb"
	shell:
		"""
		module load VCFtools/0.1.15-foss-2016b-Perl-5.24.1
		ulimit -c unlimited
		vcftools --vcf {input} --remove-filtered-all --recode  --max-missing 1 -c > {output}
		"""

