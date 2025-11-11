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
   - `--overwrite` - overwrites existing file outputs

   **Output:**  
   The output clustering of this file will be located at  
   `./wcc-networks/<method>/<dataset>/<dataset>_<base>_control.tsv`
   
3. wcc-postprocess.py
4. get-accuracy.py
5. plot-accuracy.py
