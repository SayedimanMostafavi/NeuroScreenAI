import pandas as pd

from common.preprocessing import EEGPreprocessor
from config import RESULTS_DIR


def main():

    train = pd.read_csv(
        RESULTS_DIR / "train.csv"
    )

    processor = EEGPreprocessor()

    print("\n" + "=" * 70)
    print("PREPROCESSING CHECK")
    print("=" * 70)

    for i, row in train.iterrows():

        raw = processor.run(row.file)

        print(
            f"[{i + 1:03d}/{len(train)}] "
            f"{row.filename}"
        )

        print(
            f"   Channels : {len(raw.ch_names)}"
        )

        print(
            f"   Sampling : {raw.info['sfreq']} Hz"
        )

        print(
            f"   Duration : {raw.times[-1]:.1f} sec"
        )

        print(
            f"   Channel Names:"
        )

        print(
            ", ".join(raw.ch_names)
        )

        print("-" * 70)

    print("\n" + "=" * 70)
    print("PREPROCESSING COMPLETED")
    print("=" * 70)


if __name__ == "__main__":
    main()
