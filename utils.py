monthsUa = {
  '01': 'січня',
  '02': 'лютого',
  '03': 'березня',
  '04': 'квітня',
  '05': 'травня',
  '06': 'червня',
  '07': 'липня',
  '08': 'серпня',
  '09': 'вересня',
  '10': 'жовтня',
  '11': 'листопада',
  '12': 'грудня',
}


# date format is mm/dd/yyyy
def getUADateWithDate(date):
    # string with day + monthsUa value + year
    dateUa = date.split('/')[1].lstrip('0') + ' ' + monthsUa[date.split('/')[0]] + ' ' + date.split('/')[2]
    return dateUa
