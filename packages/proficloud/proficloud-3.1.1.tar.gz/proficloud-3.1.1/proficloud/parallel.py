import multiprocessing
from joblib import Parallel, delayed



def parallel_for(func, for_range, n_jobs=None):
    if n_jobs is None:
        n_jobs = multiprocessing.cpu_count()
    return Parallel(n_jobs=n_jobs, require='sharedmem')(
        delayed(func)(i) for i in for_range
    )

def parallel_foreach(items, func, n_jobs=None):
    if n_jobs is None:
        n_jobs = multiprocessing.cpu_count()
    return Parallel(n_jobs=n_jobs, require='sharedmem')(
        delayed(func)(i) for i in items
    )
