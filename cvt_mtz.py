import argparse
import zipfile
import os
import tempfile
import shutil
from pathlib import Path


def rename_zip(folder_path: Path):
    # Duyệt từng file
    for path_in in folder_path.rglob('*'):
        # Nếu là zip, giải nén và lặp lại xử lí
        if zipfile.is_zipfile(path_in):
            dirs = os.path.join(folder_path, path_in.stem)
            os.makedirs(dirs, exist_ok=True)
            with zipfile.ZipFile(path_in, 'r') as zfp:
                zfp.extractall(dirs)
            os.remove(path_in)
            rename_zip(Path(dirs))


def cvt_mtz(mtz_path, output_zip_path):
    temp_dir = tempfile.mkdtemp(prefix="mtz_tmp_")
    temp_path = Path(temp_dir)

    try:
        # Giải nén file .mtz
        with zipfile.ZipFile(mtz_path, 'r') as zin:
            zin.extractall(temp_dir)

        # Chuyển đổi file .mtz
        rename_zip(temp_path)

        # Nén thành file zip và lưu
        with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zout:
            for file in temp_path.rglob('*'):
                arcname = file.relative_to(temp_path)
                zout.write(str(file), str(arcname))

        print(f"Da chuyen doi thanh: {output_zip_path}")

    finally:
        shutil.rmtree(temp_dir)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=".mtz converter.")
    parser.add_argument("-f",metavar="input_mtz", help="Duong dan den file .mtz", required=True)
    parser.add_argument("-s" ,metavar="output_zip", help="Duong dan den file .zip output", required=True)
    args = parser.parse_args()

    cvt_mtz(Path(args.f), Path(args.s))
