"""
Unit tests for sacc2eventsfile.py
"""
from utils.sacc2eventsfile import convert_sacc_to_workload_row, _get_dtime

def test_convert_sacc_to_workload():
    """Test"""

    # Set up
    input_row = "1003,756,21,1703688808,1703987306,1704129658,142352,COMPLETED"
    first_submit_time = 1703688806
    input_row_dict = {'JobID': '1003',
                        'NCPUS': '756',
                        'NNodes': '21',
                        'Submit': '1703688808',
                        'Start': '1703987306',
                        'End': '1704129658',
                        'ElapsedRaw': '142352',
                        'State': 'COMPLETED'}

    # Act
    result = convert_sacc_to_workload_row(input_row_dict, first_submit_time)

    output_row = "-dt 2 -e submit_batch_job | -J jobid_1003 -sim-walltime 5 --uid=user4 -t 00:01:00 -n 1 --ntasks-per-node=1 -A account2 -p normal -q normal pseudo.job"

    # Assert
    assert result == output_row

def test_get_dtime_first():
    """Return the start time since simulator start for the
    job submission"""
    first_start_time = 1703688808
    input_submit = 1703688808

    dtime = _get_dtime(input_submit, first_start_time)
    assert dtime == 0


def test_get_dtime_first():
    """Return the start time since simulator start for the
    job submission"""
    first_start_time = 1703688808
    input_submit = 1703688908

    dtime = _get_dtime(input_submit, first_start_time)
    assert dtime == 100
