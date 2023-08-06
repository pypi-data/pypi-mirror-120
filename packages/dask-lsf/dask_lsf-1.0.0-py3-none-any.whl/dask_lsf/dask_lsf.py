"""Main module."""

from dask.distributed import Client
from dask_jobqueue import LSFCluster

def setuplsfcluster(queue:str, project_id:str, memory:int, ncores:int, job_extra:str=None) -> LSFCluster:
    '''
    Helper function to create LSF Client using DASK module.

    Parameters
    ----------
    queue : str
        LSF Queue
    project_id : str
        Project ID. Gets passed to -P argument.
    memory : int
        Memory per core in GB.
    ncores : int
        Number of cores per LSF job.
    job_extra : str
        LSF String Override argument.Default -- '-R "select[mem >= memory*1000 ] rusage [mem=mem*1000]"']

    Returns
    -------
    cluster : LSFCluster
    '''

    # User config
    processes = ncores
    cores = ncores

    # Defaults
    ncpus = 1
    header_skip = ['-M']
    death_timeout = 300
    nanny = True
    walltime = '2:00'

    # Build LSF string
    lsfmem = str( memory*1000)
    lsf_mem_string = [f'-R "select[mem >= {lsfmem} ] rusage [mem={lsfmem}]"']
    if job_extra:
        job_extra = [job_extra]
    else:
        job_extra = [lsf_mem_string]

    # Create LSF Cluster
    memory = str(memory)+'GB'
    use_stdin = True
    cluster = LSFCluster(
                queue=queue, project=project_id, memory=memory,
                use_stdin=use_stdin, processes=processes, walltime=walltime,
                cores=cores, ncpus=ncpus, death_timeout=death_timeout, nanny=nanny,
                header_skip=header_skip, job_extra = job_extra
              )

    return cluster

def setuplsfclient(cluster:LSFCluster)->Client:
    '''
    Helper function to create LSF client.

    Parameters
    ----------
    cluster : LSFCluster
        LSFCluster setup for connecting to LSF jobs

    Returns
    -------
    client : Client
    '''

    timeout = 300
    direct_to_workers = False

    client = Client(
                cluster,
                timeout=timeout,
                direct_to_workers=direct_to_workers,
            )

    return client

def get_dashboard_port(client:Client) -> None:
    '''
    Returns port on which dask dashboard is running.

    Parameters
    ----------
    client : Client
        LSFClient to which LSFCluster it connected.

    Returns
    -------
    int
    '''

    return client.scheduler_info()['services']['dashboard']

def launchlsfjobs(cluster:LSFCluster, njob:int)->None:
    '''
    Helper function to launch LSF jobs.

    Parameters
    ----------
    cluster : LSFCluster
        LSFCluster setup for connecting to LSF jobs
    njobs : int
        Number of jobs to scale upto.

    Returns
    -------
    None
    '''

    cluster.scale(jobs=njob)

def waitforworkers(client:Client, n:int)->None:
    '''
    Helper function to wait for given number of workers before executing rest of the code.

    Parameters
    ----------
    client : Client
        LSFClient to which LSFCluster it connected.
    n : int
        Number of workers to wait before executing rest of the code.

    Returns
    -------
    None
    '''

    client.wait_for_workers(n)


def setupsystem(queue:str, project_id:str, memory:int, ncores:int, njobs:int, wait_for_workers:int=None, job_extra:str=None) -> (LSFCluster, Client):
    '''
    Helper function to setup connection to LSF farm using DASK module.

    Parameters
    ----------
    queue : str
        LSF Queue
    project_id : str
        Project ID. Gets passed to -P argument.
    memory : int
        Memory per core in GB.
    ncores : int
        Number of cores per LSF job.
    njobs : int
        Number of LSF jobs.
    wait_for_workers : int, default None
        Number of LSF jobs to run before executing code.
        By default the code does not wait for any lsf job.
    job_extra : str, default  '-R "select[mem >= memory*1000 ] rusage [mem=mem*1000]"']
        LSF String Override argument

    Returns
    -------
    cluster : LSFCluster
    client  : Client
    '''

    # User config
    cluster = setuplsfcluster(queue, project_id, memory, ncores, job_extra)
    launchlsfjobs(cluster, njobs)
    client = setuplsfclient(cluster)

    if wait_for_workers: waitforworkers(wait_for_workers)

    return cluster, client

def closesystem(cluster:LSFCluster, client:Client)->None:
    '''
    Helper function to close cluster and client.

    Parameters
    ----------
    cluster : LSFCluster
        LSFCluser connected to LSF jobs.
    client : LSFClient
        LSFClient connected to LSF cluster.

    Returns
    -------
    None
    '''

    cluster.close()
    client.close()

