#!/usr/bin/env python

from KafNafParserPy import KafNafParser
from subprocess import Popen, PIPE
from shutil import rmtree
from tempfile import mkdtemp
import argparse
import glob
import sys
import os

__this_folder__ = os.path.realpath(os.path.dirname(__file__))
__gold_filename__ = 'gold'
__system_filename__ ='system'
__sense_mapping__ = 'sense_mappings'
__evaluator_script__ = __this_folder__+'/score.py'

def get_max_from_list(this_list):
    if len(this_list) == 0:
        return None, None
    new_list = []
    for label, value in this_list:
        if value == 'U':
            return 'U',0
        else:
            new_list.append((label, float(value)))
    return sorted(new_list, key=lambda t: -t[1])[0]

def extract_data_file(filename, label_gold, label_system, this_temp_folder=None):
    if this_temp_folder is None:
        temp_folder = mkdtemp()
    else:
        temp_folder = this_temp_folder
        
    fd_gold = open(temp_folder+'/'+__gold_filename__,'a')
    fd_system = open(temp_folder+'/'+__system_filename__, 'a')
    
    input_obj = KafNafParser(filename)
    for term in input_obj.get_terms():
        #Get gold
        term_id = term.get_id()
        results_gold = []
        results_system = []
        for ext_ref in term.get_external_references():
            resource = ext_ref.get_resource()
            if resource == label_gold:
                results_gold.append((ext_ref.get_reference(),ext_ref.get_confidence()))
            elif resource == label_system:
                results_system.append((ext_ref.get_reference(),ext_ref.get_confidence()))
        
        if len(results_gold) > 0:
            best_gold_label, best_gold_value = get_max_from_list(results_gold)
            fd_gold.write(filename+'\t'+term_id+'\t'+best_gold_label+'\n')
            
            best_system_label, best_system_value = get_max_from_list(results_system)
            if best_system_label is not None:
                fd_system.write(filename+'\t'+term_id+'\t'+best_system_label+'\n')
    fd_gold.close()
    fd_system.close()
    
    #Create the "fake" sense.mappings
    fd_map = open(temp_folder+'/'+__sense_mapping__,'w')
    fd_map.close()
    return temp_folder
         
def run_evaluation(this_folder):
    cmd = ['python']
    cmd.append(__evaluator_script__)
    cmd.append(this_folder+'/'+__system_filename__)
    cmd.append(this_folder+'/'+__gold_filename__)
    cmd.append(this_folder+'/'+__sense_mapping__)
    evaluator = Popen(' '.join(cmd), stdin=PIPE, stdout=PIPE, stderr=PIPE, shell = True)
    evaluator.wait()
    output = evaluator.stdout.read()
    #error = evaluator.stderr.read()
    #print>>sys.stderr,'error:',error
    return output
    
    
    
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description = "Performs WSD evaluation of KAF/NAF files")
    parser.add_argument('-g','-gold', dest='label_gold', help='Resource label of the gold standard annotations in the external resource elements', required = True)
    parser.add_argument('-s','-system', dest = 'label_system', help='Resource label of the system annotations in the external resource elements', required = True)
    parser.add_argument('-i', dest = 'input_folder', help='Input folder where all the files are stored', required = True)
    parser.add_argument('-o', dest= 'out_fd', type=argparse.FileType('w'), help='File where to store the evaluation (default standard output')
    
    args = parser.parse_args()
    
    
    list_filenames = glob.glob(args.input_folder+'/*')
    
    my_temp_folder = None
    for this_filename in list_filenames:
        my_temp_folder = extract_data_file(this_filename, args.label_gold, args.label_system, this_temp_folder = my_temp_folder)  #The temp folder will be created only once
    output = run_evaluation(my_temp_folder)
    rmtree(my_temp_folder)
    
    
    
    if args.out_fd is not None:
        out = args.out_fd
        print "Evaluation output in file", out.name
    else:
        out = sys.stdout
        
    print>>out,'List of filenames evaluated:'
    for f in list_filenames:
        print>>out,'\t',f
    print>>out,'Overall evaluation:',output
    
    
  
  