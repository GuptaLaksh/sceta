import json
from pathlib import Path

_cluster_name = None

def init_gp(cluster_name):
    """Initialize cluster for subsequent calls"""
    global _cluster_name
    _cluster_name = cluster_name

def gp(param_name, cluster_name=None, CONFIG_FILE=Path("config.json")):
    """Get parameter for a cluster from config file. Print error if not found."""
    cluster_name = cluster_name or _cluster_name
    
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE) as f:
            all_configs = json.load(f)
        
        if cluster_name not in all_configs:
            print(f"Error: Cluster '{cluster_name}' not found in config file")
            return None
        
        cluster_config = all_configs[cluster_name]
        if param_name not in cluster_config:
            print(f"Error: Parameter '{param_name}' not found for cluster '{cluster_name}'")
            return None
        
        return cluster_config[param_name]
    else:
        print(f"Error: Config file not found at {CONFIG_FILE}")
        return None