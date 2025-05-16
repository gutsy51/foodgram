"""Constants used in the project and applications."""

# Page sizes.
PAGE_SIZE_PRJCT = 6              # At the project level.
PAGE_SIZE_API = PAGE_SIZE_PRJCT  # At the API app level.

# REST_FRAMEWORK['DEFAULT_THROTTLE_RATES'].
DRF_THROTTLE_RATES_USER = '1000/hour'
DRF_THROTTLE_RATES_ANON = '200/hour'

# Models.
USER_AVATAR_UPLOAD_TO = 'users/profile_pictures'
RECIPE_MIN_COOKING_TIME = 1
RECIPE_IMAGE_UPLOAD_TO = 'recipes/images'
RECIPE_INGREDIENT_MIN_AMOUNT = 1
