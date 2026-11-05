from datetime import date, timedelta


def calculate_next_due_date(last_completed_date, frequency_weeks):
    return last_completed_date + timedelta(weeks=frequency_weeks)


def get_status(next_due_date):
    today = date.today()

    if next_due_date < today:
        return "OVERDUE"
    elif next_due_date == today:
        return "DUE TODAY"
    else:
        return "UPCOMING"


def get_days_text(next_due_date):
    difference = (next_due_date - date.today()).days

    if difference < 0:
        days = abs(difference)

        if days == 1:
            return "1 day overdue"

        return f"{days} days overdue"

    elif difference == 0:
        return "Due today"

    elif difference == 1:
        return "Due tomorrow"

    else:
        return f"Due in {difference} days"
