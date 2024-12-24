import datetime
import glob
from pathlib import Path
from typing import Union

import cv2
import numpy as np
from astropy.io import fits
from PIL import Image
from tqdm import tqdm

from constants import DIGITIZATION_SIZE, IMGSZ, SEGMENT_COUNT


class FitsConverter:
    def __init__(
        self,
        path_for_images: Union[str, Path],
        path_for_csv: Union[str, Path],
        glob_str: str = None,
        path_to_fits: Union[str, Path] = None,
        iso_format_fits: str = "%Y-%m-%dT%H%M%SZ",
        verbose: bool = False,
    ) -> None:
        self.time_format = "%Y-%m-%dT%H:%M:%S.%f"
        self.iso_format_fits = iso_format_fits
        self.verbose = verbose
        self.dates = []
        self.filenames = []
        self.headers = []
        self.columns = ["filename", "date", "image_width", "block", "orig_fits"]
        if path_to_fits is not None:
            self.all_filenames = sorted(list(Path(path_to_fits).glob("*.fits")))
        elif glob_str is not None:
            self.all_filenames = sorted(list(glob.glob(glob_str)))
        else:
            raise ValueError(
                "You must provide a path to fits files or a string for glob."
            )
        if len(self.all_filenames) == 0:
            raise ValueError(
                "0 .fits files were found. Please provide a correct path or string for glob."
            )
        self.all_filenames_sep = [self.all_filenames[0]]
        self.path_for_images = Path(path_for_images)
        self.path_for_csv = Path(path_for_csv)

    def convert(self) -> None:
        for idx in range(1, len(self.all_filenames)):
            now = datetime.datetime.strptime(
                Path(self.all_filenames[idx]).stem.split(".")[2], self.iso_format_fits
            )
            before = datetime.datetime.strptime(
                Path(self.all_filenames[idx - 1]).stem.split(".")[2],
                self.iso_format_fits,
            )
            if now - before >= datetime.timedelta(minutes=5):
                self.all_filenames_sep.append(self.all_filenames[idx])

        self.all_filenames = self.all_filenames_sep

        for filename in tqdm(self.all_filenames):
            try:
                file = fits.open(filename)
            except OSError as error:
                if self.verbose:
                    print(error)
                continue

            header = file[1].header

            if (
                (header["CRPIX1"] + header["R_SUN"] + 384 >= 4096)
                | (header["CRPIX2"] + header["R_SUN"] + 384 >= 4096)
                | (header["CRPIX1"] - header["R_SUN"] - 384 < 0)
                | (header["CRPIX2"] - header["R_SUN"] - 384 < 0)
            ) and self.verbose:
                print(f"{filename} - ERROR: Sun is out of bounds.")
                continue

            if (header["MISSVALS"] > 0) and self.verbose:
                print(f"{filename} - ERROR: File contains missing values")
                continue

            if (
                (header["DATAMEAN"] < 195) | (header["DATAMEAN"] > 318)
            ) and self.verbose:
                print(f"{filename} - ERROR: File is corrupted.")
                continue

            date_iso = header["DATE-OBS"]
            date = datetime.datetime.strptime(date_iso, self.time_format).replace(
                microsecond=0
            )

            self.dates += [date]
            self.filenames += [filename]
            self.headers += [header]

        self.dates = np.array(self.dates)
        self.filenames = np.array(self.filenames)

        ind = np.argsort(self.dates)
        dates_sorted = self.dates[ind]
        filenames_sorted = self.filenames[ind]
        n_fn = len(filenames_sorted)
        data = np.empty((n_fn, 5), dtype=object)

        self.path_for_images.mkdir(parents=True, exist_ok=True)

        for k_ in tqdm(range(n_fn)):
            try:
                filename = filenames_sorted[k_]
                boundary_filename = f"{Path(filename).stem}_boundary.png"
                data[k_, 1] = dates_sorted[k_]
                data[k_, 4] = str(filename)
                data[k_, 0] = boundary_filename

                file = fits.open(filename)
                header = file[1].header
                image = file[1].data

                image = np.clip(
                    image, np.quantile(image, 0.01), np.quantile(image, 0.9965)
                )
                cv2.normalize(image, image, 0, 255, cv2.NORM_MINMAX)
                image = image.astype(np.uint8)

                # cut out boundary
                rad = np.linspace(header["R_SUN"], header["R_SUN"] + 384, 384)[::-1]
                phi = np.linspace(
                    0, 2 * np.pi, int(2 * np.pi * (header["R_SUN"] + 384))
                )
                x_idx = (header["CRPIX1"] + np.outer(rad, np.cos(phi))).astype(
                    np.uint16
                )
                y_idx = (header["CRPIX2"] + np.outer(rad, np.sin(phi))).astype(
                    np.uint16
                )
                boundary = image[y_idx, x_idx]
                data[k_, 2] = boundary.shape[1]

                image_pil = Image.fromarray(boundary)

                image_pil.save(self.path_for_images / boundary_filename)
            except Exception:
                filename = filenames_sorted[k_]
                data[k_, 1] = dates_sorted[k_]
                data[k_, 4] = str(filename)
                data[k_, 0] = "CORRUPT"
                data[k_, 2] = 0
                if self.verbose:
                    print(f"{filename} - ERROR: File is corrupted.")

        diff = [delta.seconds for delta in np.diff(data[:, 1])]
        cnt_block = 0

        data[0, 3] = 0
        for i_ in range(1, n_fn):
            if diff[i_ - 1] > 6 * 60 + 100:
                cnt_block += 1
            data[i_, 3] = cnt_block

        data[:, 3] = data[:, 3].astype(int)
        self.path_for_csv.parent.mkdir(parents=True, exist_ok=True)
        np.savetxt(
            self.path_for_csv,
            data,
            header="".join([col + ", " for col in self.columns])[:-2],
            comments="",
            delimiter=", ",
            fmt="%s",
        )


class YOLOConverter:
    def __init__(
        self,
        path_for_images: Union[str, Path],
        path_for_csv: Union[str, Path],
        glob_str: str = None,
        path_to_images: Union[str, Path] = None,
        verbose: bool = False,
    ) -> None:
        self.path_for_images = Path(path_for_images)
        self.path_for_csv = Path(path_for_csv)
        if path_to_images is not None:
            self.all_filenames = sorted(list(Path(path_to_images).glob("*.png")))
        elif glob_str is not None:
            self.all_filenames = sorted(list(glob.glob(glob_str)))
        else:
            raise ValueError(
                "You must provide a path to fits files or a string for glob."
            )
        if len(self.all_filenames) == 0:
            raise ValueError(
                "0 .fits files were found. Please provide a correct path or string for glob."
            )
        self.verbose = verbose

    def convert(self) -> None:
        self.path_for_images.mkdir(parents=True, exist_ok=True)
        for filename in tqdm(self.all_filenames):
            long_image = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
            SEGMENTS_START = np.arange(SEGMENT_COUNT) * (
                DIGITIZATION_SIZE // SEGMENT_COUNT
            )
            for start in SEGMENTS_START:
                cut_image = np.hstack(
                    [
                        long_image[
                            :,
                            start : start + IMGSZ,
                        ],
                        long_image[
                            :,
                            0 : max(0, (start + IMGSZ) - long_image.shape[1]),
                        ],
                    ]
                )
                cv2.imwrite(
                    self.path_for_images
                    / (
                        str(Path(filename).stem).split(".")[2]
                        + f"_{start//(DIGITIZATION_SIZE//SEGMENT_COUNT)}.png"
                    ),
                    cut_image,
                )
