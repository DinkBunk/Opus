import io
import torchaudio
import torch
import numpy as np
from scipy.fft import fft
from pydub import AudioSegment
from pydub.utils import make_chunks
from torchaudio.transforms import MFCC, Spectrogram

default_sample_rate = 44100  # default sample rate for most audio


def chunkify(path: str, chunk_length_ms=2000):
    # Load wav file and return it as a list of tensors
    audio_segment = AudioSegment.from_wav(path)
    chunks = make_chunks(audio_segment, chunk_length_ms)
    return [audiosegment_to_tensor(chunk) for chunk in chunks]


def audiosegment_to_tensor(audio_segment):
    # Export AudioSegment to in-memory binary file
    binary_file = io.BytesIO()
    audio_segment.export(binary_file, format="wav")
    binary_file.seek(0)

    # Load the binary file with torchaudio
    waveform, sample_rate = torchaudio.load(binary_file)

    return waveform


def apply_stft(waveform, n_fft=400, hop_length=200):
    stft_transform = Spectrogram(n_fft=n_fft, hop_length=hop_length)
    return stft_transform(torch.tensor(waveform))


def apply_mfcc(waveform, sample_rate=default_sample_rate):
    mfcc_transform = MFCC(sample_rate=sample_rate)
    return mfcc_transform(torch.tensor(waveform))


def fft_transform(waveform):
    return np.abs(fft(waveform))


def ident_transform(audio_segment):
    samples = audio_segment.get_array_of_samples()
    waveform = np.array(samples).astype(np.float32)
    return waveform


transforms = {
    'Original': lambda x: x,
    'FFT': fft_transform,
    'STFT': apply_stft,
    'MFCC': apply_mfcc,
}


def apply_transform(filename, transform_name):
    # Load the audio file
    waveform, sample_rate = torchaudio.load(filename)

    # Apply the transform
    if transform_name in transforms:
        transformed_waveform = transforms[transform_name](waveform)
    else:
        raise ValueError(f'Invalid transform name: {transform_name}')

    # Convert the transformed waveform to a list for JSON serialization
    transformed_waveform_list = transformed_waveform.tolist()

    return transformed_waveform_list


def predict(filename, your_model=None):
    # Load the audio file
    waveform, sample_rate = torchaudio.load(filename)

    # Run the prediction (replace with your prediction code)
    prediction = your_model.predict(waveform)

    # If prediction is not JSON serializable, convert it to a suitable format
    # For example, if it's a NumPy array, you can convert it to a list
    if isinstance(prediction, np.ndarray):
        prediction = prediction.tolist()

    return prediction
