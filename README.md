_your zenodo badge here_

# Pringle-etal_2024_JAMES

**Coupled Lake-Atmosphere-Land Parametric Uncertainties in a Great Lakes Regional Climate Model**

William Pringle<sup>1\*</sup> and [COMPASS-GLM Team 1](https://compass.pnnl.gov/GLM/Team)

<sup>1 </sup> Environmental Science Division, Argonne National Laboratory, Lemont, IL, USA

\* corresponding author:  wpringle@anl.gov

## Abstract
In this paper the authors develop a long-term global energy-economic model which is capable of assessing alternative energy evolutions over periods of up to 100 years. The authors have sought to construct the model so that it can perform its assigned task with as simple a modelling system as possible. The model structure is fully documented and a brief summary of results is given.

## Journal reference
Pringle, W. J., Wang, J., Huang, C., Xue, P., Kayastha, M., Chakraborty, T. C., et al. (2024). Coupled Lake-Atmosphere-Land Parametric Uncertainties in a Great Lakes Regional Climate Model. Submitted to Journal of Advances in Modeling Earth Systems, ESSOAr DOI to add.

## Code reference
Pringle W. J. (2024, March XX). Project/repo:v0.1.0 (Version v0.1.0). [Zenodo](http://doi.org/some-doi-number/zenodo.7777777).

## Data reference
Pringle W. J. (2024, March XX). Great Lakes WRF-FVCOM model ensemble outputs: Summer 2018 daily LST and T2m [Data set]. [Zenodo](http://doi.org/some-doi-number/zenodo.7777777)

## Contributing modeling software
| Model | Version | Author-Year | DOI |
|-------|---------|-----------------|-----|
 FVCOM | v41 | Chenfu Huang (2023a) | [Zenodo](http://doi.org/10.5281/zenodo.7574673)
 WRF | v4.2.2  | Chenfu Huang (2023b) | [Zenodo](http://doi.org/10.5281/zenodo.7574675)


## Reproduce my experiment
1. Install the software components required to conduct the experiment from [Contributing modeling software](#contributing-modeling-software)
2. Run the following script in the `workflow` directory to re-create the input configuration matrix for the training ensemble:
   
| Script Name | Description | How to Run |
| --- | --- | --- |
| `make_perturbations.py` | preprocessing step before WRF-FVCOM model runs | `python3 make_perturbations.py` |
3. Setup directories for each ensemble member and WRF `namelist` and FVCOM `run.nml`  with the physics options specified in the output from Step 2. Use initial/boundary conditions from [ERA5](http://doi.org/10.24381/cds.adbb2d47) for the time period 05/12/2018 to 08/31/2018. Execute runs. 
4. Run the following Juptyer notebook scripts in the `workflow` directory to postprocess the WRF-FVCOM model output data:

| Script Name | Description | How to Run |
| --- | --- | --- |
| `step_one.py` | Script to run the first part of my experiment | `python3 step_one.py -f /path/to/inputdata/file_one.csv` |
| `step_two.py` | Script to run the last part of my experiment | `python3 step_two.py -o /path/to/my/outputdir` |

## Reproduce my analysis and figures
- Follow the steps to [reproduce the experiment](#reproduce-my-experiment) (Steps 1 & 3 are not trivial) --OR-- download the postprocessed output [data](#data-reference) from my experiment.
- Run the following Juptyer notebook scripts found in the `workflow` directory to reproduce the analysis and figures from the publication.

| Script Name | Description | How to Run |
| --- | --- | --- |
| `compare.py` | Script to compare my outputs to the original | `python3 compare.py --orig /path/to/original/data.csv --new /path/to/new/data.csv` |


