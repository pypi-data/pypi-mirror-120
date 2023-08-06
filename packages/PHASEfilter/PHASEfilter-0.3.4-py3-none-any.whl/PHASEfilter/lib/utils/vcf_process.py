'''
Created on 13/05/2020

@author: mmp
'''

import collections
try:
	import vcf
except ImportError as error:
	raise ImportError("{}.\nPlease run: $ pip3 install -r requirements.txt".format(error))
from PHASEfilter.lib.utils.util import NucleotideCodes, Utils

_Info = collections.namedtuple('Info', ['id', 'num', 'type', 'desc', 'source', 'version'])

class CountAlleles(object):
	
	def __init__(self, threshold_remove_variant_ad = -1.0):
		self.equal_allele = 0					## Heterozygous (Removed)
		self.diff_allele = 0					## Keep alleles
		self.loh_allele = 0						## LOH alleles
		self.pass_variation = 0					## Other than SNP
		self.dont_have_hit_postion = 0			## Don't have hit position
		self.total_alleles = 0					
		self.could_not_fetch_vcf_record = 0		## Could Not Fetch VCF Record on Hit
		self.filter_threshold_ratio_AD = 0		## remove a variant if not reach this AD ratio
		self.threshold_remove_variant_ad = threshold_remove_variant_ad ## threshold to filter
		
	def add_equal(self):
		self.equal_allele += 1
	
	def add_diff(self):
		self.diff_allele += 1
		
	def add_LOH(self):
		self.loh_allele += 1

	def add_pass_variation(self):
		self.pass_variation += 1
		
	def add_dont_have_hit_postion(self):
		self.dont_have_hit_postion += 1

	def add_could_not_fetch_vcf_record(self):
		self.could_not_fetch_vcf_record += 1
		
	def add_allele(self, value_to_add = 1):
		self.total_alleles += value_to_add
		
	def add_filter_threshold_ratio_AD(self, value_to_add = 1):
		self.filter_threshold_ratio_AD += value_to_add
		
	def has_saved_variants(self):
		"""
		:out True if there is any variants that are saved in out file 
		"""
		return (self.could_not_fetch_vcf_record + self.diff_allele +\
			self.dont_have_hit_postion + self.pass_variation +\
			self.filter_threshold_ratio_AD) > 0
			
	def has_removed_variants(self):
		"""
		:out True if any variants are removed
		"""
		return self.equal_allele > 0

	def has_loh_allele(self):
		"""
		:out True if any loh variants
		"""
		return self.loh_allele > 0
	
	def get_header(self):
		"""
		:out header
		"""
		return "Heterozygous (Removed)\tKeep alleles\tLOH alleles\tOther than SNP\tDon't have hit position" +\
			"\tCould Not Fetch VCF Record on Hit" +\
			("\tVariants removed by AD threshold {:.2f}".format(self.threshold_remove_variant_ad) if \
			self.threshold_remove_variant_ad != -1.0 else "") +\
			"\tTotal alleles\tTotal Alleles new Source VCF"
	
	def __add__(self, other):
		self.equal_allele += other.equal_allele
		self.diff_allele += other.diff_allele
		self.loh_allele += other.loh_allele
		self.pass_variation += other.pass_variation
		self.dont_have_hit_postion += other.dont_have_hit_postion
		self.total_alleles += other.total_alleles
		self.could_not_fetch_vcf_record += other.could_not_fetch_vcf_record
		self.filter_threshold_ratio_AD += other.filter_threshold_ratio_AD
		return self

	def add_line(self, line):
		lst_data = line.split()
		if (len(lst_data) == 10 or len(lst_data) == 11):
			self.equal_allele += int(lst_data[0])
			self.diff_allele += int(lst_data[1])
			self.loh_allele += int(lst_data[2])
			self.pass_variation += int(lst_data[3])
			self.dont_have_hit_postion += int(lst_data[4])
			self.could_not_fetch_vcf_record += int(lst_data[5])
		## without AD filter
		if len(lst_data) == 10:
			self.total_alleles += int(lst_data[6])
		## with AD filter 
		if len(lst_data) == 11:
			self.filter_threshold_ratio_AD += int(lst_data[6])
			self.total_alleles += int(lst_data[7])
		
	def __str__(self):
		"""
		:out statistics results
		"""
		if (self.threshold_remove_variant_ad != -1.0):
			return "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(self.equal_allele, self.diff_allele, 
				self.loh_allele, self.pass_variation, self.dont_have_hit_postion,
				self.could_not_fetch_vcf_record, self.filter_threshold_ratio_AD, 
				self.total_alleles,
				self.could_not_fetch_vcf_record + self.diff_allele +\
				self.dont_have_hit_postion + self.pass_variation)
		else:
			return "{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format(self.equal_allele, self.diff_allele, 
				self.loh_allele, self.pass_variation, self.dont_have_hit_postion,
				self.could_not_fetch_vcf_record, self.total_alleles,
				self.could_not_fetch_vcf_record + self.diff_allele +\
				self.dont_have_hit_postion + self.pass_variation)

class VcfProcess(object):
	'''
	classdocs
	'''

	### nucleotide matching bases
	nucleotide_codes = NucleotideCodes()
	utils = Utils()
	
	def __init__(self, file_name, threshold_heterozygous_ad, threshold_remove_variant_ad, b_print_results = True):
		'''
		:param file name of vcf file
		'''
		self.file_name = file_name
		self.is_zipped = True if not self.file_name is None and self.file_name.endswith(".gz") else False 
		self.threshold_heterozygous_ad = threshold_heterozygous_ad
		self.threshold_remove_variant_ad = threshold_remove_variant_ad
		self.b_print_results = b_print_results
		self.count_alleles = CountAlleles(threshold_remove_variant_ad)
		self.temp_file_reference = self.utils.get_temp_file("refererence_get_bases_", ".txt")

	def __del__(self):
		"""
		remove temp files
		"""
		self.utils.remove_file(self.temp_file_reference)

	def exist_meta_data_tag(self, meta_data_tag):
		"""
		:param meta tag name; name to test if exists in VCF header
		"""
		if (self.is_zipped): handle_in = open(self.file_name, 'rb')
		else: handle_in = open(self.file_name, 'r')
		try:
			vcf_reader = vcf.Reader(handle_in, compressed=self.is_zipped)
			tag_to_test = "##" + meta_data_tag.lower() + "="
			for header_file in vcf_reader._header_lines:
				if header_file.lower().startswith(tag_to_test): return True
		except Exception as e:
			pass
		finally:
			handle_in.close()
		return False

	def exist_reference_name(self, reference_file_name):
		"""
		:param reference_file_name; reference file name without path
		
		## from VCF file example
		### ##reference=file:///usr/share/databases/references/candida/albicans_SC5314/v_22/C_albicans_SC5314_A22_chromosomes.fasta
		"""
		if (self.is_zipped): handle_in = open(self.file_name, 'rb')
		else: handle_in = open(self.file_name, 'r')
		try:
			vcf_reader = vcf.Reader(handle_in, compressed=self.is_zipped)
			
			for header_file in vcf_reader._header_lines:
				if header_file.lower().startswith('##reference'):
					file_name = header_file.split('/')[-1]
					return file_name.split('/')[-1].lower() == reference_file_name.split('/')[-1].lower()
		except Exception as e:
			pass
		finally:
			handle_in.close()
		return False

	def get_reference_name(self):
		"""
		:param reference_file_name; reference file name without path
		
		## from VCF file example
		### ##reference=file:///usr/share/databases/references/candida/albicans_SC5314/v_22/C_albicans_SC5314_A22_chromosomes.fasta
		"""
		if (self.is_zipped): handle_in = open(self.file_name, 'rb')
		else: handle_in = open(self.file_name, 'r')
		try:
			vcf_reader = vcf.Reader(handle_in, compressed=self.is_zipped)
			
			for header_file in vcf_reader._header_lines:
				if header_file.lower().startswith('##reference'):
					file_name = header_file.split('/')[-1]
					return file_name.split('/')[-1]
		except Exception as e:
			pass
		finally:
			handle_in.close()
		return ""
			
	def get_ratio(self, vect_data, count_base):
		"""
		:param vect_data [#REF, #ALT1, #ALT2, ...] 
		return ratio of AD
		"""
		if (len(vect_data) == 0): return 1.0
		n_ref = vect_data[0]
		if (count_base < len(vect_data)):
			n_alt = vect_data[count_base]
			if (n_alt == 0): return 0.0
			try:
				return float("{:.2f}".format(n_alt / (sum(vect_data[1:]) + n_ref))) 
			except ZeroDivisionError:
				return 1.0
		return 0.5

		
	def has_format(self, format_tag_to_test):
		"""
		:param test if a format tag exist, can be 'AD', GT, 'DP', ...
		"""
		TEST_COUNT_AD = 5
		count_AD = 0
		lines = 0
		if (self.is_zipped): handle_in = open(self.file_name, 'rb')
		else: handle_in = open(self.file_name, 'r')
		try:
			vcf_reader = vcf.Reader(handle_in, compressed=self.is_zipped)
			
			for record in vcf_reader:
				if (record.is_snp or record.is_indel):
					sample = record.samples[0]
					if (format_tag_to_test in sample.data._fields):
						count_AD += 1
						if (count_AD == TEST_COUNT_AD): break

					lines += 1
					if lines > 10: break
		except Exception as e:
			pass
		finally:
			handle_in.close()
		return count_AD == TEST_COUNT_AD or lines == count_AD
	
	def has_info(self, format_tag_to_test):
		"""
		:param test if a format tag exist, can be 'AD', GT, 'DP', ...
		"""
		TEST_COUNT_AC = 5
		count_AC = 0
		lines = 0
		if (self.is_zipped): handle_in = open(self.file_name, 'rb')
		else: handle_in = open(self.file_name, 'r')
		try:
			vcf_reader = vcf.Reader(handle_in, compressed=self.is_zipped)
			
			for record in vcf_reader:
				if (record.is_snp or record.is_indel and format_tag_to_test in record.INFO):
					count_AC += 1
					if (count_AC == TEST_COUNT_AC): break

					lines += 1
					if lines > 10: break
		except Exception as e:
			pass
		finally:
			handle_in.close()
		return count_AC == TEST_COUNT_AC or lines == count_AC


	def remove_this_record(self, record, record_hit, position_hit, lift_over_ligth):
		"""
		:param record  vcf line from vcf source
		:param record_hit  vcf line from vcf hit
		:param position_hit hit position in hit chromosome
		:param lift_over_ligth object to get sequence from the references
		:out True if this record is heterozygous
		"""
		is_allele_heterozygous = False	## default
		equal_alts = 0
		count_base = 0
		for alt_base_in_hit in record_hit.ALT:
			alt_base_in_hit_str = str(alt_base_in_hit)

			### test heterozygous
			if (len(record.samples) > 0):
				### on the reference only look for the first one
				sample = record.samples[0]

				### calculate ratio if necessary
				if (self.threshold_heterozygous_ad != -1.0 and 'AD' in sample.data._fields):
					index = sample.data._fields.index('AD')
					ratio_ad = self.get_ratio(sample.data[index], 1)	### ratio to define Hetero and Homo
					if (self.b_print_results): print("Ratio: ", record, "->",  record_hit, ratio_ad)
					
					### define heterozygous or homozygous
					if (self.threshold_heterozygous_ad >= ratio_ad):
						is_allele_heterozygous = True
				else:
					if ('AC' in record.INFO and record.INFO['AC'][0] == 1):
						is_allele_heterozygous = True

			### test wildcard in alt base
			if (alt_base_in_hit_str == '*'):
				count_base += 1
				continue	### skip wildcard
			
			if (record_hit.POS == position_hit and record.REF == alt_base_in_hit_str and \
				record_hit.REF in record.ALT and is_allele_heterozygous):
				# record(CHROM=Ca22chr1A_C_albicans_SC5314, POS=42343, REF=T, ALT=[C])
				# record_hit(CHROM=Ca22chr1B_C_albicans_SC5314, POS=42344, REF=C, ALT=[T])
				
				### now is necessary to calculate the gap between alignments
				if (record.is_indel):
					if (self.test_indel_equal(record, record_hit.REF, record_hit, alt_base_in_hit_str, lift_over_ligth)):
						if (self.b_print_results): print("EQUAL: ", record.heterozygosity, record, "->", record_hit.heterozygosity,
							record_hit, ": is_allele_heterozygous ", str(is_allele_heterozygous))
					else:
						if (self.b_print_results): print("DIFF: ", record.heterozygosity, record, "->", record_hit.heterozygosity,
							record_hit, ": is_allele_heterozygous ", str(is_allele_heterozygous))
						equal_alts += 1
				else:
					if (self.b_print_results): print("EQUAL: ", record.heterozygosity, record, "->", record_hit.heterozygosity,
						record_hit, ": is_allele_heterozygous ", str(is_allele_heterozygous))
			else:
				### save in an output
				if (self.b_print_results): print("DIFF: ", record.heterozygosity, record, "->", record_hit.heterozygosity,
						record_hit, ": is_allele_heterozygous ", str(is_allele_heterozygous))
				equal_alts += 1

			count_base += 1
		### if at least one equal allele keep this record
		return equal_alts == 0


	def is_loh(self, record, record_hit, position_hit, lift_over_ligth):
		"""
		Test if a variant is LOH
		:param record  vcf line from vcf source
		:param record_hit  vcf line from vcf hit
		:param position_hit hit position in hit chromosome
		:param lift_over_ligth object to get sequence from the references
		:out True if this record is heterozygous
		"""
		is_allele_heterozygous = False	## default
		equal_alts = 0
		count_base = 0
		for alt_base_in_hit in record_hit.ALT:
			alt_base_in_hit_str = str(alt_base_in_hit)

			### test heterozygous
			if (len(record.samples) > 0):
				sample = record.samples[0]	### always first sample

				### calculate ratio if necessary
				if (self.threshold_heterozygous_ad != -1.0 and 'AD' in sample.data._fields):
					index = sample.data._fields.index('AD')
					ratio_ad = self.get_ratio(sample.data[index], 1)	### ratio to define Hetero and Homo
					if (self.b_print_results): print("Ratio: ", record, "->",  record_hit, ratio_ad)
					
					### define heterozygous or homozygous
					if (self.threshold_heterozygous_ad >= ratio_ad):
						is_allele_heterozygous = True
				else:
					if ('AC' in record.INFO and record.INFO['AC'][0] == 1):
						is_allele_heterozygous = True

			### test wildcard in alt base
			if (alt_base_in_hit_str == '*'):
				count_base += 1
				continue	### skip wild card

			## only change not before is_allele_heterozygous
			if (record_hit.POS == position_hit and record.REF == alt_base_in_hit_str and \
				record_hit.REF in record.ALT and not is_allele_heterozygous):
				# record(CHROM=Ca22chr1A_C_albicans_SC5314, POS=42343, REF=T, ALT=[C])
				# record_hit(CHROM=Ca22chr1B_C_albicans_SC5314, POS=42344, REF=C, ALT=[T])

				### test for INDEL
				if (record.is_indel):
					if (self.test_indel_equal(record, record_hit.REF, record_hit, alt_base_in_hit_str, lift_over_ligth)):
						if (self.b_print_results): print("EQUAL: ", record.heterozygosity, record, "->",  record_hit.heterozygosity, record_hit)
					else:
						if (self.b_print_results): print("DIFF: ", record.heterozygosity, record, "->",  record_hit.heterozygosity, record_hit)
						equal_alts += 1
				else:	## test for SNP
					if (self.b_print_results): print("EQUAL: ", record.heterozygosity, record, "->",  record_hit.heterozygosity, record_hit)
			else:
				### save in an output
				if (self.b_print_results): print("DIFF: ", record.heterozygosity, record, "->",  record_hit.heterozygosity, record_hit)
				equal_alts += 1

			count_base += 1
		### if at least one equal allele keep this record
		return equal_alts == 0


	def test_indel_equal(self, record, alt_base_in_source, record_hit, alt_base_in_hit, lift_over_ligth):
		"""
		Test if records has the real gaps between source and hit 
		"""
		slice_length = 20
		last_slice_source = -1
		last_slice_hit = -1
		if (self.b_print_results): print("*" * 40)
		while True:
			if (self.b_print_results):
				print("*" * 10)
				print("record.CHROM: {}".format(record.CHROM))
				print("record.POS: {}".format(record.POS))
				print("record.POS+slice_length: {}".format(record.POS+slice_length))
				print("record_hit.CHROM: {}".format(record_hit.CHROM))
				print("record_hit.POS: {}".format(record_hit.POS))
				print("record_hit.POS+slice_length: {}".format(record_hit.POS+slice_length))
			
			### get sequence from the reference source
			slice_source = lift_over_ligth.reference_from.get_base_in_position(\
					record.CHROM, record.POS, record.POS+slice_length, self.temp_file_reference)
			### get sequence from the reference hit
			slice_hit = lift_over_ligth.reference_to.get_base_in_position(\
					record_hit.CHROM, record_hit.POS, record_hit.POS+slice_length, self.temp_file_reference)
			
			### count difference bases
			(length_bases_after_base_source, length_bases_after_base_hit) = self.get_length_bases_match(
				slice_source, slice_hit, record.REF, alt_base_in_source, record_hit.REF, alt_base_in_hit)
			
			### testing
			if (length_bases_after_base_hit >= 0 and length_bases_after_base_source >= 0):
				if (length_bases_after_base_hit > length_bases_after_base_source):
					return (length_bases_after_base_hit ==\
						length_bases_after_base_source + (len(record_hit.REF) - len(alt_base_in_hit)) )
				else:
					return (length_bases_after_base_hit + (len(record.REF) - len(alt_base_in_source)) ==\
						length_bases_after_base_source)

			### increase length if didn't found match
			slice_length += 20
			if ((last_slice_source > -1 and len(slice_source) == last_slice_source) \
				or slice_length > 300): return False 
			if ((last_slice_hit > -1 and last_slice_hit == len(slice_hit)) \
				or slice_length > 300): return False
			last_slice_source = len(slice_source)
			last_slice_hit = len(slice_hit)
		return False


	def get_length_bases_match(self, slice_source, slice_hit, ref_source, alt_base_in_source, ref_hit, alt_base_in_hit):
		"""
		:param slice_source "GAAAAAAAAAAAGTGAAAATC"
		:param slice_hit "GAAAAAAAAAAAAGTGAAAAT"
		:param ref_source "G"
		:param alt_base_in_source "GA"
		:param ref_hit "GA"
		:param alt_base_in_hit "G"
		:out (length_bases_after_base_source, length_bases_after_base_hit) return the length of the match sequence
			OR (-1,-1) if reach the end of the slice
		"""
		if (self.b_print_results):
			print("*" * 5)
			print("slice_source: " + slice_source)
			print("slice_hit: " + slice_hit)
			print("ref_source: " + ref_source)
			print("alt_base_in_source: " + alt_base_in_source)
			print("ref_hit: " + ref_hit)
			print("alt_base_in_hit: " + alt_base_in_hit)

		if (len(ref_source) < len(alt_base_in_source)):	### case "G" -> "GA"
			length_bases_after_base_source = self._get_length_bases_match(slice_source, ref_source, alt_base_in_source)
		else:
			length_bases_after_base_source = self._get_length_bases_match(slice_source, alt_base_in_source, ref_source)
			
		if (len(ref_hit) < len(alt_base_in_hit)):	### case "G" -> "GA"
			length_bases_after_base_hit = self._get_length_bases_match(slice_hit, ref_hit, alt_base_in_hit)
		else:
			length_bases_after_base_hit = self._get_length_bases_match(slice_hit, alt_base_in_hit, ref_hit)
		return (length_bases_after_base_source, length_bases_after_base_hit)

		
	def _get_length_bases_match(self, slice_seq, ref, alt_base):
		"""
		:out -1 if reach slice limit without get a different alt base
			number of alt bases
		"""
		length_bases_after_base_ = 0
		base_on_repeat = alt_base[len(ref): len(alt_base)]
		for _ in range(len(ref), len(slice_seq), len(alt_base) - len(ref)):
			if (base_on_repeat == slice_seq[_: _ + len(base_on_repeat)]):
				length_bases_after_base_ += len(base_on_repeat)
			else:
				return length_bases_after_base_
		return -1

		
	def match_vcf_to(self, seq_name_a, lift_over_ligth, vcf_hit, seq_name_b, vcf_out,
					vcf_out_removed_temp, vcf_out_LOH_temp):
		"""
		:out nothing
		"""
		if (self.is_zipped): handle_in = open(self.file_name, 'rb')
		else: handle_in = open(self.file_name, 'r')
		try:
			
			with open(vcf_out, 'w') as handle_vcf_out, open(vcf_out_removed_temp, 'w') as handle_vcf_remove_out,\
					open(vcf_out_LOH_temp, 'w') as handle_vcf_LOH_out, open(vcf_hit, 'rb') as handle_hit:
				vcf_reader = vcf.Reader(handle_in, compressed=self.is_zipped)
				vcf_reader_hit = vcf.Reader(handle_hit, compressed=True)
				vcf_write = vcf.VCFWriter(handle_vcf_out, vcf_reader)
				vcf_write_removed = vcf.VCFWriter(handle_vcf_remove_out, vcf_reader)
				vcf_write_LOH = vcf.VCFWriter(handle_vcf_LOH_out, vcf_reader)
				
				for record in vcf_reader:
					if (record.is_snp or record.is_indel):
						#print(record.heterozygosity, record)
						
						## remove variant if is low AD and user define it
						sample = record.samples[0]
						if self.threshold_remove_variant_ad != -1.0 and 'AD' in sample.data._fields:
							index = sample.data._fields.index('AD')
							ratio_ad = self.get_ratio(sample.data[index], 1)
							if (self.threshold_remove_variant_ad > ratio_ad):
								self.count_alleles.add_filter_threshold_ratio_AD()
								continue
						
						### get the position
						(position, position_most_left) = lift_over_ligth.get_best_pos_in_target(seq_name_a, seq_name_b, record.POS)
						if (position != -1):		### has position in opposite chromosome
							
							### start read from last position
							count_record = 0
							for record_hit in vcf_reader_hit.fetch(seq_name_b, position -1, position):
								count_record += 1
								if not self.remove_this_record(record, record_hit, position, lift_over_ligth):
									vcf_write.write_record(record)
									self.count_alleles.add_diff()
									
									### test LOH
									if self.is_loh(record, record_hit, position, lift_over_ligth):
										vcf_write_LOH.write_record(record)
										self.count_alleles.add_LOH()
								else:
									self.count_alleles.add_equal()
									vcf_write_removed.write_record(record)
							if (count_record == 0):
								self.count_alleles.add_could_not_fetch_vcf_record()
								if (self.b_print_results):
									print("Error FetchRecord: ", record.heterozygosity, record)
									print("Position from: {}    Position To: {}".format(record.POS, position))
								vcf_write.write_record(record)
						else:
							### save in an output
							if (self.b_print_results):
								print("Erro Pos: ", record.heterozygosity, record)
								print("Position hit: {}    Position most left: {}".format(position, position_most_left))
							vcf_write.write_record(record)
							self.count_alleles.add_dont_have_hit_postion()
					else:
						self.count_alleles.add_pass_variation()
						vcf_write.write_record(record)
					
					### add one allele
					self.count_alleles.add_allele()
					
				#### save statistics results
				if (self.b_print_results):
					print(self.count_alleles.get_header()) 
					print(self.count_alleles)
		except Exception as e:
			pass
		finally:
			handle_in.close()


	def parse_vcf(self, file_result, vect_pass_ref, lift_over_ligth):
		"""
		:param file_result - output file
		:param vect_pass_ref - don't parse this chr
		:param lift_over_ligth - method to pass, ref_a is always the main reference
		:out line processed
		"""
		
		TAG_TO_ADD = "start_hit"
		
		tem_file = self.utils.get_temp_file("syncronize", ".vcf")
		chr_name = ""	### nothing processed yet
		chr_name_B = ""
		(lines_parsed, lines_failed_parse) = (0, 0)
		vect_fail_synch = []
		
		if (self.is_zipped): handle_in = open(self.file_name, 'rb')
		else: handle_in = open(self.file_name, 'r')
		try:
			with open(tem_file, 'w') as handle_vcf_out:
				vcf_reader = vcf.Reader(handle_in, compressed=self.is_zipped)
				vcf_reader.infos[TAG_TO_ADD] = _Info(id=TAG_TO_ADD, num=1, type='Integer', 
					source=None, version=None, desc=\
					'Has the synchronize position from the reference {} to {}'.format(\
					lift_over_ligth.reference_from.get_reference_name(),
					lift_over_ligth.reference_to.get_reference_name()))
				vcf_write = vcf.VCFWriter(handle_vcf_out, vcf_reader)
				
				for record in vcf_reader:
					## {'line_index': 34, 'line_raw': 'chrI\tS01\tTY1/TY2_soloLTR\t36933\t37200\t.\t+\t.\tID=TY1/TY2_soloLTR:chrI:36933-37200:+;Name=TY1/TY2_soloLTR:chrI:36933-37200:+\n', 
					## 'line_status': 'normal', 'parents': [], 'children': [], 'line_type': 'feature', 'directive': '', 'line_errors': [], 'type': 'TY1/TY2_soloLTR', 'seqid': 'chrI', 'source': 'S01', 'start': 36933, 'end': 37200, 'score': '.', 'strand': '+', 'phase': '.', 
					## 'attributes': {'ID': 'TY1/TY2_soloLTR:chrI:36933-37200:+', 'Name': 'TY1/TY2_soloLTR:chrI:36933-37200:+'}}
	
					### if failed synch save line and continue
					if (record.CHROM in vect_fail_synch):
						vcf_write.write_record(record)
						continue
						
					## test chr_name		
					if (chr_name != record.CHROM):
						chr_name = record.CHROM
						if (chr_name.lower() in vect_pass_ref): continue	### chr to not process
						
						chr_name_B = lift_over_ligth.reference_to.get_chr_in_genome(chr_name)
						if chr_name_B is None:
							vect_fail_synch.append(record.CHROM)
							continue
				
						if (not lift_over_ligth.synchronize_sequences(chr_name, chr_name_B)):
							vcf_write.write_record(record)
							vect_fail_synch.append(record.CHROM)
							continue
						
					### test positions
					result_start = -1
					if (self.utils.is_integer(record.POS)):
						### parse positions
						(result_start, result_most_left_start) = lift_over_ligth.get_best_pos_in_target(chr_name, chr_name_B, int(record.POS))
						
					### save new position
					if (result_start != -1):
						### Add StartHit info
						record.add_info(TAG_TO_ADD, value="{}".format(result_start))
						vcf_write.write_record(record)
						lines_parsed += 1
					else:
						vcf_write.write_record(record)
						lines_failed_parse += 1
		except Exception as e:
			pass
		finally:
			handle_in.close()
				
		### compress or copy
		if (file_result.endswith(".gz")): 
			self.utils.compress_file(tem_file, file_result)
			self.utils.remove_file(tem_file)
		else: self.utils.move_file(tem_file, file_result)
		
		return (lines_parsed, lines_failed_parse, vect_fail_synch)


