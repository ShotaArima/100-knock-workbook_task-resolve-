import os
import urllib.request
import zipfile
from pathlib import Path
from colorama import Fore, Style


def main():
    print("[Start] Setup")
    target_url = "http://www3.shuwasystem.co.jp/support/download/7142/DA_WB.zip"
    zip_file_name = "DA_WB.zip"
    extract_dir = "data"

    # 1. ダウンロード
    download_data(target_url, zip_file_name)

    # 2. 解凍
    unzip(zip_file_name, extract_dir)

    # 3. 完了メッセージ & zipファイル削除
    print("[Complete] Setup finished.")
    os.remove(zip_file_name)
    print(f"Removed temporary file: {zip_file_name}")

def download_data(url: str, save_path: str):
    """
    指定されたURLからファイルをダウンロードする
    """
    if os.path.exists(save_path):
        print(f"File already exists at {save_path}, skipping download.")
        return
    else:
        print(f"Downloading from {url}...")
    
        # パスからディレクトリ部分を抽出
        dir_name = os.path.dirname(save_path)
        
        # ディレクトリ名が空（カレントディレクトリ）でない場合のみ作成
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        
        # ダウンロード実行
        urllib.request.urlretrieve(url, save_path, progress_print)
        print(f"Downloaded and saved to: {save_path}")


def progress_print(block_count, block_size, total_size):
    percentage = 100.0 * block_count * block_size / total_size
    # 100より大きいと見た目が悪いので……
    if percentage > 100:
            percentage = 100
    # バーはmax_bar個で100％とする
    max_bar = 50
    bar_num = int(percentage / (100 / max_bar))
    progress_element = '=' * bar_num
    if bar_num != max_bar:
            progress_element += '>'
    bar_fill = ' ' # これで空のとこを埋める
    bar = progress_element.ljust(max_bar, bar_fill)
    total_size_kb = total_size / 1024
    print(
        Fore.LIGHTCYAN_EX,
        f'[{bar}] {percentage:.2f}% ( {total_size_kb:.0f}KB )\r',
        end='')
    print('') # 改行
    print(Style.RESET_ALL, end="")

def unzip(zip_path: str, extract_to: str):
    """
    ZIPファイルを解凍する
    """
    
    print(f"Unzipping {zip_path}...")
    # 解凍先のディレクトリを作成
    os.makedirs(extract_to, exist_ok=True)
    
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for info in zip_ref.infolist():
            # 1. 元のファイル名を cp437 (zip標準の生バイト) でデコードしてから cp932 (Shift-JIS) でデコードし直す
            # これにより日本語名が正しく復元されます
            try:
                filename = info.filename.encode('cp437').decode('cp932')
            except:
                filename = info.filename # 変換できない場合はそのまま

            # 2. 展開先のフルパスを作成
            target_path = Path(extract_to) / filename
            
            # ディレクトリの場合は作成して次へ
            if info.is_dir():
                target_path.mkdir(parents=True, exist_ok=True)
                continue
            
            # ファイルの場合はディレクトリを作ってから書き込み
            target_path.parent.mkdir(parents=True, exist_ok=True)
            with zip_ref.open(info) as source, open(target_path, "wb") as target:
                target.write(source.read())

    print(f"Extracted and converted all files to: {extract_to}")


if __name__ == "__main__":
    main()
