"""climaticai."""
import warnings

# hack to prevent warnings from skopt
# must import sklearn first
import sklearn
import climaticai.model_family
import climaticai.objectives
import climaticai.pipelines
import climaticai.preprocessing
import climaticai.problem_types
import climaticai.utils
from climaticai.utils import print_info, update_checker

with warnings.catch_warnings():
    warnings.simplefilter("ignore", FutureWarning)
    warnings.simplefilter("ignore", DeprecationWarning)
    import skopt
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)

__version__ = "0.33.0"
