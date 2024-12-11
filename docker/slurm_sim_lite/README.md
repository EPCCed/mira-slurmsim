# Slurm Simulator Docker and Apptainer Containers

There are two dockerfiles provided, one builds a standalone container that only runs the simulator 
with associated input data. The other is couple with a JupyterLab/Rstudio instance and can be used
to run the analyses jointly with the simulation. 

I prefer the standalone version as it keeps the container image minimal. 

A docker compose file is provided for easu



```bash
# Build the relevant Docker image
docker build -f docker/slurm_sim_lite/slurm_sim_lite.Dockerfile -t slurm_sim_lite .
```

For building the JupyterLab enabled image, refer to: 
https://github.com/ubccr-slurm-simulator/slurm_sim_tools/tree/v3.0-branch/tutorials

The basic docker container does not have bind-mounted directories, therefore any data
generated will not be persistent once the container exists. To main data persistence from
simulation runs, use the docker compose file:

