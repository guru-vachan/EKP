from enum import Enum

class IndexType(str, Enum):

    FLAT_L2 = "flat_l2"

    FLAT_IP = "flat_ip"

    HNSW = "hnsw"