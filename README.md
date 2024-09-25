## Slurm Simulator - MIRA

This project uses and adapts the SLURM Simulator Tool to run simulations of the Cirrus cluster (and other cluster configs). It is based on the tutorial section at [Slurm Sim Tools](https://github.com/ubccr-slurm-simulator/slurm_sim_tools) (See the `tutorials` folder). More cluster configs can be made by editing the config files in te `etc` folder.

The SLURM simulator itself can be found at https://github.com/ubccr-slurm-simulator/slurm_simulator

### Docker

The simulator runs in a Docker container, and can be started either using the raw `Dockerfile` or set up using the `docker-compose.yml` file which generates persistent storage in the host machine so that the output files can be analysed outwith the container.

### Generating SLURM Sim workload files

tbd
