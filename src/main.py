import pandas as pd
from tqdm import tqdm
import requests
import io
import justext
from warcio.archiveiterator import ArchiveIterator
import hashlib
import argparse


def download_page(warc_file: str, warc_offset: int, warc_length: int) -> str:
    """
    Downloads and returns the cleaned up page for a given warc url.
    """

    # prefix to all warc paths
    prefix = 'https://data.commoncrawl.org/'

    # request file as byte stream
    resp = requests.get(prefix + warc_file,
                        headers={'Range': 'bytes={}-{}'.format(warc_offset, warc_offset + warc_length - 1)})
    raw_data = io.BytesIO(resp.content)

    # get full page that contains sentence we are searching for
    page = None
    for record in ArchiveIterator(raw_data, arc2warc=True):
        rec = record.content_stream().read()
        try:
            page = rec.strip().decode('utf-8')
        except:
            page = rec.strip().decode('latin1')

    # clean up page
    paragraphs = justext.justext(page, justext.get_stoplist("English"))
    cleaned_text = " ".join(
        [paragraph.text for paragraph in paragraphs if not paragraph.is_boilerplate]
    ).replace('\n', ' ')
    return cleaned_text

def retrieve_sents(df: pd.DataFrame, out_file: str) -> pd.DataFrame:
    """
    Retrieves all sentences for a DataFrame with warc info, adds them to the DataFrame, and returns it.
    """

    # check if this is a checkpoint file, i.e. contains retrieved sentences
    if not "sentence" in df.columns:
        df["sentence"] = ["MISS"]*len(df)

    # loop over dataframe to retrieve all missing sentences
    for i, row in tqdm(df.iterrows(), total=len(df)):
        # sentence in this row was already retrieved
        if row["sentence"] != "MISS":
            continue

        # try to retrieve sentence from warc
        try:
            if row["sentence_hash"] == "29e0b7839794033e21e685773285ebdc":
                page_sent = "Err:510"  # failed to download this sentence at dataset creation
            else:
                page = download_page(row["warc_file"], row["warc_offset"], row["warc_length"])
                page_sent = page[row["sentence_offset"]:row["sentence_offset"] + row["sentence_length"]]
        except Exception:
            print("Cannot find sentence for row with index {}. Skipping.".format(str(i)))
            page_sent = ""

        # check sentence for correctness
        if hashlib.md5(page_sent.encode("utf-8")).hexdigest() != row["sentence_hash"]:
            print("Missmatch. Original: {}, new: {}".format(row["sentence"], page_sent))

        # add sentence to dataset
        df.at[i, "sentence"] = page_sent

        # save checkpoint every 500 rows
        if i > 0 and i % 500 == 0:
            chkpt_file = out_file.replace(".tsv", ".chkpt{}.tsv".format(str(i)))
            df.to_csv(chkpt_file, sep="\t", index=False)
            print("Saved checkpoint file to start retrieving from in case of failure: {}".format(chkpt_file))

    # check how many sentences couldn't be retrieved
    print("{} sentences could not be retrieved successfully.".format(str(len(df[df["sentence"] == "MISS"]))))
    return df

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Completes the Few Shot Dataset with sentences from the respective '
                                                 'WARC files')
    parser.add_argument('-i', '--in-file', help='Path to the input file (e.g. ./data/test_full_no_sents.tsv)',
                        required=True)
    parser.add_argument('-o', '--out-file', help='Path to the input file (e.g. ./data/test_full.tsv)',
                        required=True)
    args = parser.parse_args()

    # read in file
    df = pd.read_csv(args.in_file, sep="\t", float_precision='round_trip')

    # retrieve all sents for the file from the archive
    df = retrieve_sents(df, args.out_file)

    # write out the new file with completed sentence info
    df.to_csv(args.out_file, sep="\t", index=False)