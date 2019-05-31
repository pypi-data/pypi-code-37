(
    ColrControl('test', 'red')
    .write(delay=0.25)
    .move_ret()
    .blue('this')
    .write(delay=0.25)
)
(
    ColrControl('this', 'blue', style='bold')
    .write(delay=0.25)
    .blue('thing')
    .write(delay=0.25)
)

print('\nFinished.\n')
