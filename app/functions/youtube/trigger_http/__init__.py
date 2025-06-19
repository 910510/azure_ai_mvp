import logging
from logic import run_logic

import azure.functions as func

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("Run Http Request!")
    
    try:
        run_logic()
        return func.HttpResponse(f"✅ 수동 실행 완료", status_code=200)
    except Exception as e:
        logging.error(str(e))
        return func.HttpResponse(f"❌ 오류: {str(e)}", status_code=500)