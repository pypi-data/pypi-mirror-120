from curtsies import Input

def dialog(bgcolor='cyan',options=['1', '2', '3'],limit=3):
  if bgcolor== 'black':
    bgcolor = '\x1b[40m'
  elif bgcolor == 'red':
    bgcolor = '\x1b[41m'
  elif bgcolor == 'green':
    bgcolor = '\x1b[42m'
  elif bgcolor == 'yellow':
    bgcolor = '\x1b[43m'
  elif bgcolor == 'blue':
    bgcolor = '\x1b[44m'
  elif bgcolor == 'purple':
    bgcolor = '\x1b[45m'
  else:
    bgcolor = '\x1b[46m'

  opt = ['\033[F']
  opt = opt+options
  opt_sel = bgcolor
  opt_end = '\x1b[49m'
  opt.insert(1, opt_sel)
  opt.insert(3, opt_end)
  sel_index = 0
  print('\n',*opt, sep="  ")
  with Input(keynames='curtsies') as karl:
      for key in Input():
        if key == "<RIGHT>":
          sel_index = sel_index + 1
          if sel_index >= limit:
            sel_index = limit-1
        elif key == "<LEFT>":
          sel_index = sel_index - 1
          if sel_index < 0:
            sel_index = 0
        elif key == "<Ctrl-j>":
          break
        if ('\x1b[49m' in opt) == True:
          opt.remove(bgcolor)
          opt.remove('\x1b[49m')
        opt.insert(sel_index+1, opt_sel)
        opt.insert(sel_index+3, opt_end)
        print(*opt, sep="  ")
  return(sel_index)