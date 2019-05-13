from datetime import datetime, timedelta

start = datetime.strptime('23:14','%H:%M')
end = datetime.strptime('03:34', '%H:%M')
print('   start', start)

total = end - start  # wrong

print('1. end  ', end)
print('   total', total)
print('   seconds', total.seconds)
print('   total_seconds', total.total_seconds())

if end < start: # correct
    end += timedelta(days=1)
total = end - start

print('2. end  ', end)
print('   total', total)
print('   seconds', total.seconds)
print('   total_seconds', total.total_seconds())

rounded_up_hours = round((total.total_seconds() + 1800.)/3600.)

print('rounded_up_hours', rounded_up_hours)
