import traceback

from gui import RotoView

try:
    rotoview = RotoView()
    rotoview.mainloop()

except Exception as e:
    with open('log.txt', 'a') as f:
        f.write(str(e))
        f.write(traceback.format_exc())
        raise e

