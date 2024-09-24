"""sacc2eventsfile.py

This utility converts raw accounting data from the SLURM accounting
database and converts it into the "events file" format that is used
in the SLURM Simulator. The events file is a plain text file where 
each row represents a job submission entry similar to what would be
found in an sbatch submission command or script.
"""
import csv
from random import randint


SACCFILE = "/home/decval/devel/slurm_sim_mira/test/2024_Q1_CPU-sacct-subset.csv"
NEW_WORKLOAD_FILE = "q1events.events"

UID_PREFIX = "user"
UID_RANGE = 5
# dt time in slurm sim can be too long if measured in seconds on real 
# accounting data.
# Use this factor to divide through
DT_FACTOR = 1


def convert_sacc_to_workload_row(row: dict, first_submit_time: int) -> str:
    """
    Convert a sacc entry to a workload entry
    """

    job_string = (
        f"-dt {_get_dtime(row['Submit'], first_submit_time)} "
        f"-e submit_batch_job | "
        f"-J jobid_{row['JobID']} "
        f"-sim-walltime {(row['ElapsedRaw'])} "
        f"--uid={_get_uid()} "
        f"-t {_get_request_time()} "
        f"-n {int(row['NNodes'])} "
        f"--ntasks-per-node={_get_ntasks_per_node(row['NCPUS'], row['NNodes'])} "
        f"-A {_get_account()} -p {_get_priority()} -q {_get_queue()} pseudo.job"
    )
    return job_string


def _get_dtime(submit_time, first_submit_time) -> int:
    dtime = int(submit_time) - int(first_submit_time)
    if DT_FACTOR > 1:
      return dtime/DT_FACTOR
    else:
      return dtime

def _get_sim_walltime(elapse: int):
    return int(elapse)/60

def _get_uid():
    randuid = randint(1, UID_RANGE)
    uid = UID_PREFIX + str(randuid)
    return uid

def _get_request_time():
    return "00:01:00"

def _get_ntasks_per_node(cpus, nodes):
    """Calculates no of tasks per node
    
    Usage examples:
    >>> _get_ntasks_per_node(60, 3)
    20
    >>> _get_ntasks_per_node(56, 3)
    18
    """
    return int(cpus) // int(nodes)

def _get_account():
    rand_account_id = randint(1, 2)
    account_id = "account" + str(rand_account_id)
    return account_id

def _get_priority():
    return "normal"

def _get_queue():
    return "normal"

def process_sacc():
    """
    Process a complete Slurm sacct file into a 
    slurm simulator events file."""
    # Open an input and the new output file
    with (open(SACCFILE, 'r', encoding="utf-8") as csvfile,
          open(NEW_WORKLOAD_FILE, 'w', encoding="utf-8") as outputfile):
        print("Reading in SACC file")
        sacc_reader = csv.DictReader(csvfile, delimiter=",")
        # The outputfile is not standard csv...

        first_submit_time = 0
        row_count = 0
        for row in sacc_reader:
            if row_count == 0:
                first_submit_time = row["Submit"]
                first_row = convert_sacc_to_workload_row(row, first_submit_time)
                outputfile.writelines(first_row + "\n")
                row_count = 1
            else:
                new_row = convert_sacc_to_workload_row(row, first_submit_time)
                outputfile.writelines(new_row + "\n")

if __name__ =="__main__":
    process_sacc()
