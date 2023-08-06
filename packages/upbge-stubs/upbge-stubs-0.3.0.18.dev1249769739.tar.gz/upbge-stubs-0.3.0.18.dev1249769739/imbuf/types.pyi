"""


Image Buffer Types (imbuf.types)
********************************

This module provides access to image buffer types.

:class:`ImBuf`

"""

import typing

class ImBuf:

  """"""

  def copy(self) -> ImBuf:

    ...

  def crop(self, min: typing.Any, max: typing.Any) -> None:

    """

    Crop the image.

    """

    ...

  def free(self) -> None:

    """

    Clear image data immediately (causing an error on re-use).

    """

    ...

  def resize(self, size: typing.Any, method: str = 'FAST') -> None:

    """

    Resize the image.

    """

    ...

  channels: int = ...

  """

  Number of bit-planes.

  """

  filepath: str = ...

  """

  filepath associated with this image.

  """

  planes: int = ...

  """

  Number of bits associated with this image.

  """

  ppm: typing.Any = ...

  """

  pixels per meter.

  """

  size: typing.Any = ...

  """

  size of the image in pixels.

  """
