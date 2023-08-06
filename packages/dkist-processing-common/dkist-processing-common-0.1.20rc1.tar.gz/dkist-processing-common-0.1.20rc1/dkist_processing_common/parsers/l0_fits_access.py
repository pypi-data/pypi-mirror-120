"""
By-frame 214 L0 header keywords that are not instrument specific
"""
from typing import Optional
from typing import Union

from astropy.io import fits

from dkist_processing_common.parsers.l1_fits_access import L1FitsAccess


class L0FitsAccess(L1FitsAccess):
    def __init__(
        self,
        hdu: Union[fits.ImageHDU, fits.PrimaryHDU, fits.CompImageHDU],
        name: Optional[str] = None,
        auto_squeeze: bool = True,
    ):
        super().__init__(hdu=hdu, name=name, auto_squeeze=auto_squeeze)

        # TODO rename this to IPTASK once dkist-fits-specifications gets far enough
        self.ip_task_type: str = self.header["DKIST004"]

        # TODO: replace these with new Rev E DKIST keys
        self.date_begin: str = self.header["DATE-BGN"]
        self.date_end: str = self.header["DATE-END"]
