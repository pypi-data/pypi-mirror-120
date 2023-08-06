#!/usr/bin/env python3

import os
import time

import radical.pilot as rp


def cb(task, state):
    print('== %s %s' % (task.uid, task.state))
    if state == rp.AGENT_SCHEDULING:
        print('== cancel')
        task.cancel(wait=False)


# ------------------------------------------------------------------------------
#
if __name__ == '__main__':

    with rp.Session() as session:

        pmgr    = rp.PilotManager(session=session)
        pd_init = {'resource': 'local.localhost',
                   'runtime' : 60,
                   'cores'   :  8}

        pdesc = rp.PilotDescription(pd_init)
        pilot = pmgr.submit_pilots(pdesc)
        tmgr  = rp.TaskManager(session=session)

        tmgr.add_pilots(pilot)
        tmgr.register_callback(cb)

        td = rp.TaskDescription()
        td.executable = '/bin/date'
        td.scheduler  = 'foo'

        task = tmgr.submit_tasks(td)
        task.wait()


# ------------------------------------------------------------------------------

