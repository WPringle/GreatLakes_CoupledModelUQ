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
1. Install the software components required to conduct the experiement from [Contributing modeling software](#contributing-modeling-software)
2. Download and install the supporting input data required to conduct the experiement from [Input data](#input-data)
3. Run the following scripts in the `workflow` directory to re-create this experiment:

| Script Name | Description | How to Run |
| --- | --- | --- |
| `step_one.py` | Script to run the first part of my experiment | `python3 step_one.py -f /path/to/inputdata/file_one.csv` |
| `step_two.py` | Script to run the last part of my experiment | `python3 step_two.py -o /path/to/my/outputdir` |

4. Download and unzip the output data from my experiment [Output data](#output-data)
5. Run the following scripts in the `workflow` directory to compare my outputs to those from the publication

| Script Name | Description | How to Run |
| --- | --- | --- |
| `compare.py` | Script to compare my outputs to the original | `python3 compare.py --orig /path/to/original/data.csv --new /path/to/new/data.csv` |

## Reproduce my figures
Use the scripts found in the `figures` directory to reproduce the figures used in this publication.

| Script Name | Description | How to Run |
| --- | --- | --- |
| `generate_figures.py` | Script to generate my figures | `python3 generate_figures.py -i /path/to/inputs -o /path/to/outuptdir` |
