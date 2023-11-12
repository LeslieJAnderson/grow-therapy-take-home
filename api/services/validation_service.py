import datetime
from functools import wraps

from api.services import date_service

def validate_and_convert_to_week_range(param_name):
    def decorator(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            try:
                formatted_date = datetime.datetime.strptime(kwargs[param_name], '%Y%m%d')
            except ValueError:
                return {"message": "Enter a valid date in the format of YYYYMMDD"}, 400
            
            # Overwrite param with the week range
            kwargs[param_name] = {
                'original_value': kwargs[param_name],
                'week_range': date_service.week_range_of(formatted_date)
            }
            
            return f(*args, **kwargs)
        return wrap
    return decorator

def validate_and_convert_to_month_range(param_name):
    def decorator(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            try:
                formatted_date = datetime.datetime.strptime(kwargs[param_name], '%Y%m%d')
            except ValueError:
                return {"message": "Enter a valid date in the format of YYYYMMDD"}, 400
            
            # Overwrite param with the month range
            kwargs[param_name] = {
                'original_value': kwargs[param_name],
                'month_range': date_service.month_range_of(formatted_date)
            }
            
            return f(*args, **kwargs)
        return wrap
    return decorator