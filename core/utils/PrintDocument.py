import datetime
from core.db.dbconnect import Request
from datetime import datetime
from docxtpl import DocxTemplate

def transform_date(date):
    months = ['января', 'февраля', 'марта', 'апреля', 'мая', 'июня',
              'июля', 'августа', 'сентября', 'октября', 'ноября', 'декабря']
    return f'{date.day} {months[int(date.month) - 1]} {date.year} года'

async def create_help_call(telegram_id, request: Request):
    dateNow = datetime.today()
    date_document = f'{dateNow.year}-{dateNow.month}-{dateNow.day}'
    result = await request.get_help_call_data(telegram_id, date_document)

    print(f"{telegram_id}: select * from get_data_for_document_test('{telegram_id}', '{date_document}')")
    doc = DocxTemplate("core\pattern_docs\helpCall.docx")

    startDate = datetime.strptime(f"{result[6]}", '%Y-%m-%d')
    endDate = datetime.strptime(f"{result[7]}", '%Y-%m-%d')
    subdDate = endDate - startDate

    level_education = f"{result[10]}".lower()
    context = {
        'date_create': transform_date(result[13]),
        'number_doc': result[3],
        'name_employer': result[11],
        'full_name_student': f"{result[0]} {result[1]} {result[2]}",
        'type_education': result[9],
        'name_group': result[12],
        'type_session': result[8],
        'start_date_session': transform_date(startDate),
        'end_date_session': transform_date(endDate),
        'count_days_session': subdDate.days,
        'level_education': level_education,
        'speciality': f'{result[4]} "{result[5]}"'
    }
    doc.render(context)
    filepath = f"docs\help_{result[3]}_{result[13]}.docx"
    doc.save(filepath)
    return filepath
