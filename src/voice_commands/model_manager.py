import zipfile
from io import BytesIO
from pathlib import Path

import requests
from tqdm import tqdm

ROOT = Path("~/.cache/voice_commands/models").expanduser()


def download_model(
    url: str,
    name: str,
    root: str = ROOT,
):
    root = Path(root).expanduser()
    (root / name).mkdir(parents=True, exist_ok=False)

    response = requests.get(url, stream=True)
    content_size = int(response.headers.get("content-length", 0))
    block_size = 1024

    data = BytesIO()

    with tqdm(
        total=content_size,
        unit="iB",
        unit_scale=True,
        desc=f"Downloading <{name}> from <{url}>",
    ) as pbar:
        for chunk in response.iter_content(chunk_size=block_size):
            data.write(chunk)
            pbar.update(len(chunk))

    with zipfile.ZipFile(data, "r") as file:
        with tqdm(
            total=len(data.getvalue()),
            unit="iB",
            unit_scale=True,
            desc="Extracting",
        ) as pbar:
            for file_info in file.infolist():
                file.extract(file_info, root / name)
                pbar.set_postfix(file=file_info.filename)
                pbar.update(file_info.file_size)


def list_models():
    for model_name_dir in ROOT.iterdir():
        print(model_name_dir.name)
