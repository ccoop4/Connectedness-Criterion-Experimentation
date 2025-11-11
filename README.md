# Connectedness-Criterion-Experimentation

Start by downloading networks.zip from https://databank.illinois.edu/datasets/IDB-3284069 and unzip the files into a folder called EC-SBM-Networks. You may insert other test networks into this folder, but the script is designed so that one may choose a dataset and an input clustering method and retrieve the correct EC-SBM network from this folder. Note that you should not have a "networks" folder inside the EC-SBM-Networks folder; that folder should become EC-SBM-Networks.

Next, run install-relevant-repos.sh. This will pull all relevant code needed for clustering, WCC postprocessing, and accuracy measurement.

There are four Python scripts that are intended to be run sequentially but may be run individually.

1. **control-generation.py**  
   The purpose of this script is to generate a clustering of a specified EC-SBM network that will have various WCC treatments applied to it. This clustering will not be overwritten when various WCC treatments are applied to it. The purpose of this is to be able to see if WCC treatments help at all.

   **The script takes in the following arguments:**

   - `--dataset <string>` - (required) specifies the dataset you want to analyze, e.g. `academia_edu`, will pull the EC-SBM network located at `EC-SBM-Networks/<base>/<dataset>/0/edge.tsv`
   - `--base <string>` - (required) specifies the input clustering to the specific EC-SBM network, will pull the EC-SBM network located at `EC-SBM-Networks/<base>/<dataset>/0/edge.tsv`
   - `--method <string>` - (required) specifies the treatment clustering method you want to apply, must be in `{leiden-mod | leiden-cpm | dcsbm-flat}`
   - `--resolution <float>` - (optional) use this if you are using `leiden-cpm` for the treatment method
   - `--seed <int>` - (optional) specifies a seed
   - `--random-seed` - (optional) chooses some 32-bit integer as a random seed
   - `--num-processors <int>` - (optional) default = 1
   - `--overwrite` - (optional) overwrites existing file outputs

   **Output:**  
   The output clustering of this file will be located at  
   `./wcc-networks/<method>/<dataset>/<dataset>_<base>_control.tsv`
   
2. wcc-postprocess.py
   The purpose of this script is to apply different WCC treatments to a control network generated via the previous script. The differences in the WCC treatments come down to the criterion used to determine well-connectedness. These can be specified in a list. Right now, there is no upper bound as to the amount you are able to test. They must be formatted in one of the following ways: `"C"`, `"Cn^k"`, `"Clog_b(n)"`, where C, b are integers and k is a float.

   **The script takes in the following arguments:**
   
   - `--dataset <string>` - (required) same as above
   - `--base <string>` - (required) same as above
   - `--control-method <string>` - (required) specifies which control method we should apply WCC to
   - `--control-resolution <float>` - (optional) use if you use leiden-cpm as the control method
   - `--criteria <string> <string> ...` - (required) list of strings corresponding to the criterion you want to test
   - `--num-processors <int>` - (optional) default = 1
   - `--overwrite` (optional) overwrites existing file outputs
   
     **Output:**  

   WCC outputs will be written to  
   `./wcc-networks/<control>/<dataset>/<dataset>_<base>_<criterion>.tsv`
3. **get-accuracy.py**  
   This script will compute many accuracy statistics for a specified control + WCC treatment method (treating the original EC-SBM as the ground truth). This script can either compute the global or local (only consider nodes in the WCC clustering) accuracy statistics.

   **The script takes in the following arguments:**
   - `--dataset <string>` - (required) same as above
   - `--base <string>` - (required) same as above
   - `--control-method <string>` - (required) same as above
   - `--control-resolution <float>` - (optional) same as above
   - `--num-processors <int>` - (optional) default = 1
   - `--local` - (optional) use this flag if you want to get the local accuracy
   - `--overwrite` - overwrites existing file outputs
   - `--accuracy-script <path>` - (optional) defaults to `outside_repos/network_evaluation/commdet_acc/compute_cd_accuracy.py`

   **Output:**  
   Accuracy outputs will be written to  
   `./accuracy_stats/<dataset>_<base>_<control-method>/<criterion>{_local (if local)}.<metric>`
4. **plot-accuracy.py**  
   This script will generate stacked bar charts for AMI, ARI, NMI, Precision, and Recall for a specified base-clustering/control-method pair. Each bar in each bar chart represents a different connectedness criterion.
   
   **The script takes in the following arguments:**
   - `--dataset <string>` - (required) same as above
   - `--base <string>` - (required) same as above
   - `--control-method <string>` - (required) You must include the resolution for `leiden-cpm` in this case. It must match the folder you are trying to pull the accuracy stats from.
   - `--local` - (optional) use this if you want to use the local accuracy stats, note that they must have been previously generated
   - `--output <path>` - (optional) defaults to `./plots/<dataset>_<base>_<control-method>.png`
   
   **Output:**  
   Plot outputs will be written to  
   `./plots/<dataset>_<base>_<control-method>.png`


