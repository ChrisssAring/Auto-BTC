import gzip
import shutil
with gzip.open('btc_latest.txt.gz', 'rb') as f_in:
    with open('btc_latest_cleaned.txt', 'wb') as f_out:
        shutil.copyfileobj(f_in, f_out)
