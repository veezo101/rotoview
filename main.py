import traceback

from gui import RotoView

try:
    rotoview = RotoView()
    rotoview.mainloop()

except Exception as ex:
    with open('log.txt', 'a') as f:
        f.write(str(ex))
        f.write(traceback.format_exc())
        raise ex
