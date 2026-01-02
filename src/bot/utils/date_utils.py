from datetime import datetime

class DateUtils:

    @staticmethod
    def iso_to_br_date(iso_datetime: str) -> str:
        """
        Converte uma data ISO (ex: '2025-10-18T18:10:09.529398')
        para o formato brasileiro dd/MM/yyyy.
        """
        if not iso_datetime:
            return ""

        data_iso = iso_datetime[:10]
        data_obj = datetime.strptime(data_iso, "%Y-%m-%d")

        return data_obj.strftime("%d/%m/%Y")

    @staticmethod
    def now_br_format() -> str:
        """
        Retorna a data e hora atual no formato brasileiro: dd/MM/yyyy • HH:mm
        """
        return datetime.now().strftime("%d/%m/%Y • %H:%M")