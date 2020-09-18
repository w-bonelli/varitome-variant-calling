import filter_vcfs
import createMasterVcf
filter_vcfs.filter_vcfs("input_files/BGV006865.bam.vcf",
  "input_files/BGV006865.bam.filtered.vcf",
  {"BGV006865.bam" : 43.6514})
filter_vcfs.filter_vcfs("input_files/BGV008108.bam.vcf",
  "input_files/BGV008108.bam.filtered.vcf",
  {"BGV008108.bam" : 42.0557})
