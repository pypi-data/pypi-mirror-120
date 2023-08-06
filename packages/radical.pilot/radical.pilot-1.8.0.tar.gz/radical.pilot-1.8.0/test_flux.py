#!/usr/bin/env python3

import radical.pilot as rp


# ------------------------------------------------------------------------------
#
if __name__ == '__main__':

    session = rp.Session()
    try:

        pmgr = rp.PilotManager(session=session)
        tmgr = rp.TaskManager(session=session)

        pd_init = {'resource'      : 'debug.flux',
                   'runtime'       : 30,
                   'cores'         : 128,
                  }
        pdesc = rp.PilotDescription(pd_init)
        pilot = pmgr.submit_pilots(pdesc)

        tmgr.add_pilots(pilot)

        tds = list()
        for i in range(0, 1024):

            td = rp.TaskDescription()
            td.executable    = '/bin/date'
            td.cpu_processes = 1
            tds.append(td)

        tmgr.submit_tasks(tds)
        tmgr.wait_tasks()

    finally:
        session.close(download=True)

# ------------------------------------------------------------------------------

