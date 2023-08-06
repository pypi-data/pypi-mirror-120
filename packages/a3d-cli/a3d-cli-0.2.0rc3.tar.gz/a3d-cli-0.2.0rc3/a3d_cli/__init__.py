import pkg_resources

try:
    __version__ = pkg_resources.get_distribution("a3d-cli").version
except pkg_resources.DistributionNotFound:
    __version__ = "dev"
