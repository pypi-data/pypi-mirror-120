'''
Created on 16/06/2020

@author: mmp
'''
import unittest, os
from PHASEfilter.lib.utils.util import Utils
from PHASEfilter.lib.utils.reference import Reference
from PHASEfilter.lib.utils.lift_over_simple import LiftOverLight
from PHASEfilter.lib.process.process_references import ProcessTwoReferences
from PHASEfilter.lib.utils.software import Software

class Test(unittest.TestCase):


	def test_sync(self):
	
		utils = Utils("synchronize")
		temp_work_dir = utils.get_temp_dir()
	
		seq_file_name_a = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/referenceSaccharo/S01.chrXVI.fa')
		seq_file_name_b = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/referenceSaccharo/S228C.chrXVI.fa')
		self.assertTrue(os.path.exists(seq_file_name_a))
		self.assertTrue(os.path.exists(seq_file_name_b))
	
		seq_name_a = "chrXVI"
		seq_name_b = "chrXVI"
	
		reference_a = Reference(seq_file_name_a)
		reference_b = Reference(seq_file_name_b)
		impose_minimap2_only = False
		lift_over_ligth = LiftOverLight(reference_a, reference_b, temp_work_dir, impose_minimap2_only, True)
		lift_over_ligth.synchronize_sequences(seq_name_a, seq_name_b)
		
		self.assertEqual(Software.SOFTWARE_minimap2_name, lift_over_ligth.get_best_algorithm(seq_name_a, seq_name_b))
		
		### test positions
		temp_file = utils.get_temp_file("base_name", ".fasta")
		
		### test some positions
		position_to_test = 426
		self.assertEqual((-1, -1), lift_over_ligth.get_pos_in_target(seq_name_a, seq_name_b, position_to_test))
		position_to_test = 427
		self.assertEqual((1, -1), lift_over_ligth.get_pos_in_target(seq_name_a, seq_name_b, position_to_test))
		self.assertEqual(reference_a.get_base_in_position(seq_name_a, position_to_test, position_to_test+1, temp_file),
						reference_b.get_base_in_position(seq_name_a, 1, 2, temp_file))
		position_to_test = 428
		self.assertEqual((2, -1), lift_over_ligth.get_pos_in_target(seq_name_a, seq_name_b, position_to_test))
		self.assertEqual(reference_a.get_base_in_position(seq_name_a, position_to_test, position_to_test+1, temp_file),
						reference_b.get_base_in_position(seq_name_a, 2, 3, temp_file))
		position_to_test = 10000
		self.assertEqual((9585, -1), lift_over_ligth.get_pos_in_target(seq_name_a, seq_name_b, position_to_test))
		self.assertEqual(reference_a.get_base_in_position(seq_name_a, 10000, 10001, temp_file),
						reference_b.get_base_in_position(seq_name_a, 9585, 9586, temp_file))
		self.assertNotEqual(reference_a.get_base_in_position(seq_name_a, 10000, 10001, temp_file),
						reference_b.get_base_in_position(seq_name_a, 9586, 9587, temp_file))
		position = 50000
		self.assertEqual((49610, -1), lift_over_ligth.get_pos_in_target(seq_name_a, seq_name_b, position))
		utils.remove_file(temp_file)
	
		temp_out = utils.get_temp_file("out_sync_saccharo", ".txt")
		process_two_references = ProcessTwoReferences(seq_file_name_a, seq_file_name_b, temp_out)
		process_two_references.process()
	
		out_result_expected = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/referenceSaccharo/out_sync_saccharo.txt')
	
		temp_diff = utils.get_temp_file("diff_file", ".txt")
		cmd = "diff {} {} > {}".format(temp_out, out_result_expected, temp_diff)
		os.system(cmd)
		vect_result = utils.read_text_file(temp_diff)
		self.assertEqual(0, len(vect_result))
		utils.remove_file(temp_out)
	

	def test_sync_2(self):
	
		utils = Utils("synchronize")
		temp_work_dir = utils.get_temp_dir()
	
		seq_file_name_a = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/referenceSaccharo/S01.chrXVI.fa')
		seq_file_name_b = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/referenceSaccharo/S228C.chrXVI.fa')
		self.assertTrue(os.path.exists(seq_file_name_a))
		self.assertTrue(os.path.exists(seq_file_name_b))
	
		seq_name_a = "chrXVI"
		seq_name_b = "chrXVI"
	
		reference_a = Reference(seq_file_name_a)
		reference_b = Reference(seq_file_name_b)
		impose_minimap2_only = True
		lift_over_ligth = LiftOverLight(reference_a, reference_b, temp_work_dir, impose_minimap2_only, True)
		lift_over_ligth.synchronize_sequences(seq_name_a, seq_name_b)
	
		temp_file = utils.get_temp_file("base_name", ".fasta")
	
		### test some positions
		position_to_test = 426
		self.assertEqual((-1, -1), lift_over_ligth.get_pos_in_target(seq_name_a, seq_name_b, position_to_test))
		position_to_test = 427
		self.assertEqual((1, -1), lift_over_ligth.get_pos_in_target(seq_name_a, seq_name_b, position_to_test))
		self.assertEqual(reference_a.get_base_in_position(seq_name_a, position_to_test, position_to_test+1, temp_file),
						reference_b.get_base_in_position(seq_name_a, 1, 2, temp_file))
		position_to_test = 428
		self.assertEqual((2, -1), lift_over_ligth.get_pos_in_target(seq_name_a, seq_name_b, position_to_test))
		self.assertEqual(reference_a.get_base_in_position(seq_name_a, position_to_test, position_to_test+1, temp_file),
						reference_b.get_base_in_position(seq_name_a, 2, 3, temp_file))
		position_to_test = 10000
		self.assertEqual((9585, -1), lift_over_ligth.get_pos_in_target(seq_name_a, seq_name_b, position_to_test))
		self.assertEqual(reference_a.get_base_in_position(seq_name_a, 10000, 10001, temp_file),
						reference_b.get_base_in_position(seq_name_a, 9585, 9586, temp_file))
		self.assertNotEqual(reference_a.get_base_in_position(seq_name_a, 10000, 10001, temp_file),
						reference_b.get_base_in_position(seq_name_a, 9586, 9587, temp_file))
		position = 50000
		self.assertEqual((49610, -1), lift_over_ligth.get_pos_in_target(seq_name_a, seq_name_b, position))
		self.assertEqual(reference_a.get_base_in_position(seq_name_a, position, position+1, temp_file),
						reference_b.get_base_in_position(seq_name_a, 49610, 49611, temp_file))
		utils.remove_file(temp_file)
	
	
	def test_sync_3(self):
	
		utils = Utils("synchronize")
		temp_work_dir = utils.get_temp_dir()
	
		seq_file_name_a = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/referenceSaccharo/S01.chrXVI.fa')
		seq_file_name_b = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'files/referenceSaccharo/S228C.chrXVI.fa')
		self.assertTrue(os.path.exists(seq_file_name_a))
		self.assertTrue(os.path.exists(seq_file_name_b))
	
		seq_name_a = "chrXVI"
		seq_name_b = "chrXVI"
	
		reference_a = Reference(seq_file_name_a)
		reference_b = Reference(seq_file_name_b)
		impose_minimap2_only = False
		lift_over_ligth = LiftOverLight(reference_a, reference_b, temp_work_dir, impose_minimap2_only, True)
		lift_over_ligth.synchronize_sequences(seq_name_a, seq_name_b)
	
		### impose lastz best alignment
		lift_over_ligth.dt_chain_best_method[seq_name_a + "_" + seq_name_b] = Software.SOFTWARE_lastz_name
		self.assertEqual(Software.SOFTWARE_lastz_name, lift_over_ligth.get_best_algorithm(seq_name_a, seq_name_b))
		temp_file = utils.get_temp_file("base_name", ".fasta")
	
		### test some positions
		position_to_test = 426
		self.assertEqual((-1, -1), lift_over_ligth.get_pos_in_target(seq_name_a, seq_name_b, position_to_test))
		position_to_test = 427
		self.assertEqual((1, -1), lift_over_ligth.get_pos_in_target(seq_name_a, seq_name_b, position_to_test))
		self.assertEqual(reference_a.get_base_in_position(seq_name_a, position_to_test, position_to_test+1, temp_file),
						reference_b.get_base_in_position(seq_name_a, 1, 2, temp_file))
		position_to_test = 428
		self.assertEqual((2, -1), lift_over_ligth.get_pos_in_target(seq_name_a, seq_name_b, position_to_test))
		self.assertEqual(reference_a.get_base_in_position(seq_name_a, position_to_test, position_to_test+1, temp_file),
						reference_b.get_base_in_position(seq_name_a, 2, 3, temp_file))
		position_to_test = 10000
		self.assertEqual((9585, -1), lift_over_ligth.get_pos_in_target(seq_name_a, seq_name_b, position_to_test))
		self.assertEqual(reference_a.get_base_in_position(seq_name_a, 10000, 10001, temp_file),
						reference_b.get_base_in_position(seq_name_a, 9585, 9586, temp_file))
		self.assertNotEqual(reference_a.get_base_in_position(seq_name_a, 10000, 10001, temp_file),
						reference_b.get_base_in_position(seq_name_a, 9586, 9587, temp_file))
		position = 50000
		self.assertEqual((49610, -1), lift_over_ligth.get_pos_in_target(seq_name_a, seq_name_b, position))
		self.assertEqual(reference_a.get_base_in_position(seq_name_a, position, position+1, temp_file),
						reference_b.get_base_in_position(seq_name_a, 49610, 49611, temp_file))
		utils.remove_file(temp_file)



if __name__ == "__main__":
	#import sys;sys.argv = ['', 'Test.test_to_remove']
	unittest.main() 