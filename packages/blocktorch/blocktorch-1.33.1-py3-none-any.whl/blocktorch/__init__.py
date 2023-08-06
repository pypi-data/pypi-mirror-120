"""blocktorch."""
import warnings

# hack to prevent warnings from skopt
# must import sklearn first
import sklearn
import blocktorch.model_family
import blocktorch.objectives
import blocktorch.pipelines
import blocktorch.preprocessing
import blocktorch.problem_types
import blocktorch.utils
from blocktorch.utils import print_info, update_checker

with warnings.catch_warnings():
    warnings.simplefilter("ignore", FutureWarning)
    warnings.simplefilter("ignore", DeprecationWarning)
    import skopt
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

__version__ = "0.33.0"
