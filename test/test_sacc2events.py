"""
Unit tests for sacc2eventsfile.py
"""
import re
import pytest
from utils.sacc2eventsfile import (convert_sacc_to_workload_row,
                                   _get_dtime, _get_account, DT_FACTOR)

@pytest.mark.skipif(DT_FACTOR != 1, reason="Skip if DT_FACTOR != 1")
def test_convert_sacc_to_workload():
    """Test"""

    # Set up
    # input_row = "1003,756,21,1703688808,1703987306,1704129658,142352,COMPLETED"
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

    # Assert
    # Since the uid is generated with a random digit, we can't plainly
    # assert that the strings match, but we can use a regex to check for
    # a digit in a certin place (i.e. after UID)
    assert re.match(r"-dt 2 -e submit_batch_job \| "
                    r"-J jobid_1003 -sim-walltime 142352 --uid=user\d+ -t 00:01:00 -n 21 "
                    r"--ntasks-per-node=36 -A account\d+ -p normal -q normal pseudo.job", result)
    # Assert
    #assert result == output_row


def test_get_dtime_first():
    """Return the start time since simulator start for the
    job submission"""
    first_start_time = 1703688808
    input_submit = 1703688808

    dtime = _get_dtime(input_submit, first_start_time)
    assert dtime == 0


@pytest.mark.skipif(DT_FACTOR != 1, reason="Skip if DT_FACTOR set other than 1")
def test_get_dtime_later():
    """Return the start time since simulator start for the
    job submission"""
    first_start_time = 1703688806
    input_submit = 1703688808

    dtime = _get_dtime(input_submit, first_start_time)
    assert dtime == 2

def test_get_account_id():
    """Return a string that simulates an account id
    for the job submission script."""
    # Set up
    account_strings = ("account1", "account2")

    # Act
    result = _get_account()

    # Assert
    assert result in account_strings
