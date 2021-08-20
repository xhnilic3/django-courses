from django.conf import settings

# Default redirect from index page
COURSES_LANDING_PAGE_URL = getattr(settings, 'COURSES_LANDING_PAGE_URL', 'all_active_runs')

# In run details display also future chapters that are not available yet.
COURSES_SHOW_FUTURE_CHAPTERS = getattr(settings, 'COURSES_SHOW_FUTURE_CHAPTERS', False)

# Wheather to show 404 or the details of the chapter if it has passed.
COURSES_ALLOW_ACCESS_TO_PASSED_CHAPTERS = getattr(settings, 'COURSES_ALLOW_ACCESS_TO_PASSED_CHAPTERS', True)
# Wheather to show 404 or the details of the chapter if it has passed.
COURSES_ALLOW_SUBMISSION_TO_PASSED_CHAPTERS = getattr(settings, 'COURSES_ALLOW_SUBMISSION_TO_PASSED_CHAPTERS', False)
