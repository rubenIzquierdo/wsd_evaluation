# WSD EVALUATION #

Performs evaluation of WSD on a list of KAF/NAF files using the official python script from senseval2

##Input/Output##

* Input:
  - list of KAF/NAF files
  - label of the gold standard annotations in the KAF/NAF in the external references (i.e. manual_annotation)
  - label of the system annotations in the KAF/NAF in the external references (i.e. ItMakesSense#WN-1.7.1)

* Output:
  - It will print the results of the overall evaluation for all the files together


##Step by step##

1. A temporary folder is created
2. Each input file is processed and all the gold and system annotations are extracted and concatenated in the
   same files on the temp folder
3. A fake "sense_mappings" file is created, as it expected by the official scorer. In this case it will be empty
4. The official scorer (score.py) from sval2 is launched and the results is printed
5. The temporary folder is removed

##Usage##

If you call to the `evaluate.py` script with the option `-h` you will get information about the usage:

```shell
usage: evaluate.py [-h] -g LABEL_GOLD -s LABEL_SYSTEM -i INPUT_FOLDER
                   [-o OUT_FD]

Performs WSD evaluation of KAF/NAF files

optional arguments:
  -h, --help            show this help message and exit
  -g LABEL_GOLD, -gold LABEL_GOLD
                        Resource label of the gold standard annotations in the
                        external resource elements
  -s LABEL_SYSTEM, -system LABEL_SYSTEM
                        Resource label of the system annotations in the
                        external resource elements
  -i INPUT_FOLDER       Input folder where all the files are stored
  -o OUT_FD             File where to store the evaluation (default standard
                        output
  -random               Use random heuristic for each token
```

Example of usage:
```shell
python evaluate.py -gold manual_annotation -system ItMakesSense#WN-1.7.1 -i example_files -o my_eval.txt
```

This will read and evaluate all the files under the folder `example_files`, considering the gold standard
annotations those with label `manual_annotation` in the external references (and the same for the system
annotations), and storing the result in the file `my_eval.txt`.

For a random selection you could use:
```shell
python evaluate.py -gold manual_annotation -system ItMakesSense#WN-1.7.1 -i example_files -o my_eval.txt -random
```

##Contact##
* Ruben Izquierdo
* Vrije University of Amsterdam
* ruben.izquierdobevia@vu.nl  rubensanvi@gmail.com
* http://rubenizquierdobevia.com/

##License##

Sofware distributed under GPL.v2, see LICENSE file for details.