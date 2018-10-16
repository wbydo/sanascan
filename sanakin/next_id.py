from .snksession import SNKSession

class NextIdSearchable:
    @classmethod
    def next_id(klass, id_column_name, prefix, size):
        with SNKSession() as s:
            latest = s.query(
                getattr(klass, id_column_name)
            ).order_by(
                getattr(klass, id_column_name).desc()
            ).limit(1).one_or_none()

        if not latest:
            return '{}{}'.format(prefix, '1'.zfill(size))

        latest_no = int(latest[0].replace(prefix, ''))

        return '{}{}'.format(prefix, str(latest_no + 1).zfill(size))
