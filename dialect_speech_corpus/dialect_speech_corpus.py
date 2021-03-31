"""Arabic Speech Corpus"""

from __future__ import absolute_import, division, print_function

import os

import datasets
import soundfile as sf 

_CITATION = """
"""

_DESCRIPTION = """\


```python
import soundfile as sf

def map_to_array(batch):
    speech_array, _ = sf.read(batch["file"])
    batch["speech"] = speech_array
    return batch

dataset = dataset.map(map_to_array, remove_columns=["file"])
```
"""

import soundfile as sf

class DialectSpeechCorpusConfig(datasets.BuilderConfig):
    """BuilderConfig for DialectSpeechCorpusCorpus."""

    def __init__(self, **kwargs):
        """
        Args:
          data_dir: `string`, the path to the folder containing the files in the
            downloaded .tar
          citation: `string`, citation for the data set
          url: `string`, url for information about the data set
          **kwargs: keyword arguments forwarded to super.
        """
        super(DialectSpeechCorpusConfig, self).__init__(version=datasets.Version("2.1.0", ""), **kwargs)


def map_to_array(batch):
    start, stop = batch['segment'].split('_')
    speech_array, _ = sf.read(batch["file"], start = start, stop = stop)
    batch["speech"] = speech_array
    return batch

class DialectSpeechCorpus(datasets.GeneratorBasedBuilder):
    """DialectSpeechCorpus dataset."""

    BUILDER_CONFIGS = [
        DialectSpeechCorpusConfig(name="clean", description="'Clean' speech."),
    ]

    def _info(self):
        return datasets.DatasetInfo(
            description=_DESCRIPTION,
            features=datasets.Features(
                {
                    "file": datasets.Value("string"),
                    "label": datasets.features.ClassLabel(
                        names=[
                        'EGY',
                        'NOR',
                        'GLF',
                        'LAV',
                        'MSA'
                        ]
                    )
                }
            ),
            supervised_keys=("file", "text"),
            citation=_CITATION,
        )

    def _split_generators(self, dl_manager):
        archive_path = '/workspace/data_dir/'
        return [
            datasets.SplitGenerator(name="train", gen_kwargs={"archive_path": os.path.join(archive_path, "train")}),
            datasets.SplitGenerator(name="dev", gen_kwargs={"archive_path": os.path.join(archive_path, "dev")}),
        ]

    def _generate_examples(self, archive_path):
        """Generate examples from a Librispeech archive_path."""
        wav_dir = os.path.join(archive_path, "wav")
        
        for _id, c in enumerate(os.listdir(wav_dir)):
            if os.path.isdir(f'{wav_dir}/{c}/'):
                for file in os.listdir(f'{wav_dir}/{c}/'):
                    if file.endswith('.wav'):
                        wav_path = f'{wav_dir}/{c}/{file}'
                        f = sf.SoundFile(wav_path)
                        seconds = int(len(f)) // f.samplerate
                        if seconds < 5 or seconds > 20:
                            continue 
                        example = {
                            "file": wav_path,
                            "label":c
                        }
                        yield str(_id), example
