'''
Created on 13/05/2020

@author: mmp
'''
import unittest, os
from PHASEfilter.lib.utils.util import Utils, NucleotideCodes, CountLength, Cigar
from PHASEfilter.lib.utils.reference import Reference
from PHASEfilter.lib.utils.run_extra_software import RunExtraSoftware

### run command line
# export PYTHONPATH='/home/mmp/git/PHASEfilter'
# python3 -m unittest -v tests.test_utils

class Test(unittest.TestCase):


	def setUp(self):
		pass


	def tearDown(self):
		pass

	def test_refernce_names(self):
		ref_1 = Reference()
		ref_1.vect_reference = ['aaaa', 'aaba', 'aaca']
		ref_2 = Reference()
		ref_2.vect_reference = ['aaaa', 'aaba', 'aaca']

		self.assertEqual('aaaa', ref_1.get_chr_in_genome('aaaa'))
		self.assertEqual('aaba', ref_1.get_chr_in_genome('aaba'))

		ref_1.vect_reference = ['Ca22chr1A_C_albicans_SC5314', 'aaba', 'aaca']
		ref_2.vect_reference = ['Ca22chr1B_C_albicans_SC5314', 'aaba', 'aaca']
		self.assertEqual('Ca22chr1B_C_albicans_SC5314', ref_2.get_chr_in_genome('Ca22chr1A_C_albicans_SC5314'))


	def test_tabix(self):
		utils = Utils()
		run_extra_software = RunExtraSoftware()
		
		vcf_file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/vcf/test_tabix.vcf")
		self.assertTrue(os.path.exists(vcf_file_name))
		
		temp_dir = utils.get_temp_dir()
		chr_name = 'Ca22chr1A_C_albicans_SC5314'
		(temp_out_vcf, number_of_records) = run_extra_software.get_vcf_with_only_chr(vcf_file_name, chr_name, temp_dir)
		
		self.assertEqual(2209, number_of_records)
		vect_out = run_extra_software.vcf_lines_for_position(temp_out_vcf, chr_name, 1768, 1769)
		self.assertEqual(1, len(vect_out))
		self.assertTrue(vect_out[0].startswith("Ca22chr1A_C_albicans_SC5314	1768"))
		
		vect_out = run_extra_software.vcf_lines_for_position(temp_out_vcf, chr_name, 1768, 1768)
		self.assertEqual(1, len(vect_out))
		self.assertTrue(vect_out[0].startswith("Ca22chr1A_C_albicans_SC5314	1768"))

		vect_out = run_extra_software.vcf_lines_for_position(temp_out_vcf, chr_name, 1971, 1972)
		self.assertEqual(2, len(vect_out))

		chr_name = 'Ca22chrRA_C_albicans_SC5314'
		vect_out = run_extra_software.vcf_lines_for_position(temp_out_vcf, chr_name, 1813312, 1813313)
		self.assertEqual(0, len(vect_out))
		
		chr_name = 'Ca22chrRA_C_albicans_SC5314___'
		(temp_out_vcf_2, number_of_records) = run_extra_software.get_vcf_with_only_chr(vcf_file_name, chr_name, temp_dir)
		self.assertEqual(None, temp_out_vcf_2)
		self.assertEqual(0, number_of_records)
		
		## remove dir
		utils.remove_dir(temp_dir)
		utils.remove_file(temp_out_vcf)
		utils.remove_file(temp_out_vcf + ".tbi")

	def test_tabix_2(self):
		utils = Utils()
		run_extra_software = RunExtraSoftware()
		
		vcf_file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), "files/vcf/test_tabix.vcf")
		self.assertTrue(os.path.exists(vcf_file_name))
		
		temp_dir = utils.get_temp_dir()
		chr_name = 'Ca22chrRA_C_albicans_SC5314'
		(temp_out_vcf, number_of_records) = run_extra_software.get_vcf_with_only_chr(vcf_file_name, chr_name, temp_dir)
		self.assertEqual(50, number_of_records)
		
		vect_out = run_extra_software.vcf_lines_for_position(temp_out_vcf, chr_name, 1813312, 1813313)
		self.assertEqual(1, len(vect_out))
		self.assertTrue(vect_out[0].startswith("Ca22chrRA_C_albicans_SC5314	1813312"))
		
		vect_out = run_extra_software.vcf_lines_for_position(temp_out_vcf, chr_name, 1813312, 1882546)
		self.assertEqual(2, len(vect_out))
		self.assertTrue(vect_out[0].startswith("Ca22chrRA_C_albicans_SC5314	1813312"))
		self.assertTrue(vect_out[1].startswith("Ca22chrRA_C_albicans_SC5314	1882546"))
		
		chr_name = 'Ca22chr1A_C_albicans_SC5314'
		vect_out = run_extra_software.vcf_lines_for_position(temp_out_vcf, chr_name, 1768, 1769)
		self.assertEqual(0, len(vect_out))
		
		## remove dir
		utils.remove_dir(temp_dir)
		utils.remove_file(temp_out_vcf)
		utils.remove_file(temp_out_vcf + ".tbi")

	def test_reference_bases(self):
		
		nucleotide_codes = NucleotideCodes()
		self.assertTrue(nucleotide_codes.has_this_base('W', 'A')) 
		self.assertTrue(nucleotide_codes.has_this_base('w', 'a')) 
		self.assertFalse(nucleotide_codes.has_this_base('w', 'c'))
		self.assertTrue(nucleotide_codes.has_this_base('R', 'a'))
		self.assertTrue(nucleotide_codes.has_this_base('R', 'G'))
		self.assertFalse(nucleotide_codes.has_this_base('R', 'u'))
		
		self.assertTrue(nucleotide_codes.has_this_base('Y', 'c'))
		self.assertTrue(nucleotide_codes.has_this_base('Y', 't'))
		self.assertFalse(nucleotide_codes.has_this_base('Y', 'a'))
	
	def test_count_elements(self):
		
		cigar = Cigar(['4M3D2I10M17S'])
		self.assertEqual("17\t16\t17\t14\t3\t2\t73.7", str(cigar.count_length))
		
		cigar_2 = Cigar(['27H14M3D2I10M'])
		self.assertEqual("27\t26\t27\t24\t3\t2\t82.8", str(cigar_2.count_length))
		
		count_length2 = CountLength()
		count_length2 += cigar.count_length
		count_length2 += cigar_2.count_length
		self.assertEqual("Query length\tSubject length\tmissmatch\tMatch length\tDel length\tIns length\t% Match VS Del+Ins", str(count_length2.get_header()))
		self.assertEqual("44\t42\t44\t38\t6\t4\t79.2", str(count_length2))

	def test_remove_itens_cigar(self):
		
		cigar = Cigar(['4M3D2I10M17S'])
		self.assertEqual(['4M3D2I10M17S'], cigar.get_vect_cigar_string())
		cigar.remove_itens_string(2, False)
		self.assertEqual(['2I10M17S'], cigar.get_vect_cigar_string())
		cigar.remove_itens_string(0, False)
		self.assertEqual(['2I10M17S'], cigar.get_vect_cigar_string())
		cigar.remove_itens_string(1, False)
		self.assertEqual(['10M17S'], cigar.get_vect_cigar_string())
		cigar.remove_itens_string(50, False)
		self.assertEqual([''], cigar.get_vect_cigar_string())
		
		cigar_2 = Cigar(['27H14M3D2I10M'])
		self.assertEqual(['27H14M3D2I10M'], cigar_2.get_vect_cigar_string())
		cigar_2.remove_itens_string(0, True)
		self.assertEqual(['27H14M3D2I10M'], cigar_2.get_vect_cigar_string())
		cigar_2.remove_itens_string(1, True)
		self.assertEqual(['27H14M3D2I'], cigar_2.get_vect_cigar_string())
		cigar_2.remove_itens_string(2, True)
		self.assertEqual(['27H14M'], cigar_2.get_vect_cigar_string())
		cigar_2.remove_itens_string(50, True)
		self.assertEqual([''], cigar_2.get_vect_cigar_string())

	def test_map_flags(self):
		utils = Utils()
		self.assertEqual(True, utils.is_supplementary_alignment(2048))
		self.assertEqual(True, utils.is_supplementary_alignment(2064))
		self.assertEqual(False, utils.is_supplementary_alignment(0))
		self.assertEqual(True, utils.is_read_reverse_strand(2064))
		self.assertEqual(False, utils.is_read_reverse_strand(2))


if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.test_refernce_names']
	unittest.main()



