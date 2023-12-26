from source import module


args = {
    "data file": "test.dat",
    "minimum support": 0.1,
    "minimum confidence": 0.8,
    "limit": 5,
    "write file": True,
    "parallel processing": "auto" # "always", "never", others = "auto"
}
module.training(args)
    