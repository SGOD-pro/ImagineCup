from app.ai.state import State


def ocr_cleanup(state: State) -> State:
     return state['formated_ocr']=