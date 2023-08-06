from gradio import inputs, outputs
import fastai

"""
mappings is a dictionary that maps the fastai data type to the corresponding gradio input/output interface 
and pre/post-processing step. 
"""
mappings = {
    fastai.torch_core.TensorImage: {
        "type": inputs.Image(type='file', label='input'),
        "process": lambda inp: inp.name
    },
    fastai.torch_core.TensorCategory: {
        "type": outputs.Label(num_top_classes=3, label='output'),
        "process": lambda dls, out: {dls.vocab[i]: float(out[2][i]) for i in range(len(dls.vocab))}
    }
}