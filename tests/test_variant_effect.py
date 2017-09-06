import keras
import warnings
warnings.filterwarnings('ignore')
import modelzoo
from modelzoo.data import numpy_collate
from modelzoo.variant_effects import predict_variants
import numpy as np


# TODO: We still need a way to get the model output annotation from somewhere...
# TODO: which other arguments should we use for variant effect predictions?
# Only viable model at the moment is rbp, so not offering to test anything else

def test_var_eff_pred():
    # Take the rbp model
    model_dir = "examples/rbp/"
    model = modelzoo.load_model(model_dir)
    # The preprocessor
    Extractor = modelzoo.load_extractor(model_dir)

    # Hacky: take the example arguments
    import yaml
    with open(model_dir + "test_files/test.json", "r") as f:
        exec_files_path=yaml.load(f)

    for k in exec_files_path:
        exec_files_path[k] = model_dir + "test_files/" + exec_files_path[k]

    exec_files_path_here = {}
    for k in exec_files_path:
        if k != "target_file":
            exec_files_path_here[k] = exec_files_path[k]

    # Derive a list model output labels
    model_out_annotation = np.array(list(model.model_spec['targets'].keys()))

    # Run the actual predictions
    vcf_path = model_dir + "test_files/variants.vcf"
    from concise.effects.ism import ism
    res = predict_variants(model.model, vcf_path, seq_length = 101, evaluation_function = ism, exec_files_path = exec_files_path_here,
                     extractor_function = Extractor, batch_size =32, numpy_collate = numpy_collate,
                     model_out_annotation=model_out_annotation,evaluation_function_kwargs = {"diff_type":"diff"})
