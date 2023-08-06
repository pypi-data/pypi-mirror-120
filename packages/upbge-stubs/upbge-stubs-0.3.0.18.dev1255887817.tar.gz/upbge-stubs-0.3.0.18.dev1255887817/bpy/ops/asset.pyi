"""


Asset Operators
***************

:func:`assign_action`

:func:`clear`

:func:`list_refresh`

:func:`mark`

:func:`open_containing_blend_file`

:func:`tag_add`

:func:`tag_remove`

"""

import typing

def assign_action() -> None:

  """

  Set this pose Action as active Action on the active Object

  """

  ...

def clear() -> None:

  """

  Delete all asset metadata and turn the selected asset data-blocks back into normal data-blocks

  """

  ...

def list_refresh() -> None:

  """

  Trigger a reread of the assets

  """

  ...

def mark() -> None:

  """

  Enable easier reuse of selected data-blocks through the Asset Browser, with the help of customizable metadata (like previews, descriptions and tags)

  """

  ...

def open_containing_blend_file() -> None:

  """

  Open the blend file that contains the active asset

  """

  ...

def tag_add() -> None:

  """

  Add a new keyword tag to the active asset

  """

  ...

def tag_remove() -> None:

  """

  Remove an existing keyword tag from the active asset

  """

  ...
