import pandas as pd
import pkg_resources

def load_beauty():
    resource_path = '/'.join(('data','beauty.zip'))
    return pd.read_csv(pkg_resources.resource_filename(__name__,resource_path))

def load_starbucks():
    resource_path = '/'.join(('data','starbucks.zip'))
    return pd.read_csv(pkg_resources.resource_filename(__name__,resource_path))

def load_bond():
    resource_path = '/'.join(('data','bond.zip'))
    return pd.read_csv(pkg_resources.resource_filename(__name__,resource_path))

def load_movies():
    resource_path = '/'.join(('data','movies.zip'))
    return pd.read_csv(pkg_resources.resource_filename(__name__,
                                                       resource_path))

def load_chopsticks():
    resource_path = '/'.join(('data','chopsticks.zip'))
    return pd.read_csv(pkg_resources.resource_filename(__name__,
                                                       resource_path))

def load_chopsticks_full():
    resource_path = '/'.join(('data','chopsticks_full.zip'))
    return pd.read_csv(pkg_resources.resource_filename(__name__,
                                                       resource_path))

def load_correlation_example():
    resource_path = '/'.join(('data','correlation.zip'))
    return pd.read_csv(pkg_resources.resource_filename(__name__,
                                                       resource_path))

