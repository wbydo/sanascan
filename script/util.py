# ロガー設定
from logging import getLogger,StreamHandler,DEBUG
LOGGER = getLogger(__name__)
LOGGER.setLevel(DEBUG)

HANDLER = StreamHandler()
HANDLER.setLevel(DEBUG)
LOGGER.addHandler(HANDLER)

#組み込みパッケージ
import os
import sys
import hashlib

#サードパーティパッケージ
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.dialects.mysql import insert
from natto import MeCab

path_ = os.path.abspath(
    os.path.join(
        __file__,
        '../..',))

sys.path.insert(0, path_)

#自前パッケージ
import sanakin
import sanakin.db as db
from env import TARGET_DB, RAKUTEN_TRAVEL_DIR

# 定数
DATABASE = 'mysql+pymysql://{}:{}@{}/{}?charset=utf8'.format(
      TARGET_DB['user_name'],
      TARGET_DB['password'],
      TARGET_DB['host_ip'],
      TARGET_DB['db_name']
)

ENGINE = create_engine(
    DATABASE,
    encoding='utf-8',
    echo=True
)

Session = sessionmaker(bind=ENGINE)

db.init(ENGINE)

def _insert_single_record(r):
    session = Session()

    try:
        session.add(r)
        session.commit()
    except Exception as e:
        err_code, _ = e.orig.args
        if err_code == 1062:
            LOGGER.info('格納済み')
        else:
            raise e
    finally:
        session.close()

def insert_corpus(cname, csymbol):
    c = db.Corpus(
        name=cname,
        symbol=csymbol,)

    _insert_single_record(c)

def insert_snkfile(file_path, corpus_id):
    h = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(2048 * h.block_size), b''):
            h.update(chunk)
    checksum = h.hexdigest()

    target_file = db.SNKFile(
        name=os.path.basename(file_path),
        checksum=checksum,
        corpus_id=corpus_id
    )

    LOGGER.info(f'name:\t\t{target_file.name}')
    LOGGER.info(f'checksum:\t{target_file.checksum}')
    LOGGER.info('')

    session = Session()
    query = session.query(db.SNKFile).filter(db.SNKFile.name == target_file.name)
    exists = session.query(query.exists()).scalar()
    if not exists:
        n = target_file.name
        session.add(target_file)
        session.commit()
        session.close()

        LOGGER.info(f'{n}:\t格納完了!')
        LOGGER.info('')
    else:
        in_file = query.one()
        if not in_file.checksum == target_file.checksum:
            session.close()
            raise sanakin.SNKException(
                f'DB:\t{in_file.name}\t{in_file.checksum}\n'+
                f'target:\t{target_file.name}\t{target_file.checksum}\n'+
                '一致しません!!!\n')
        else:
            LOGGER.info(f'{target_file.name}:\t格納済み!')
            LOGGER.info('')
            session.close()

def insert_original_datum(corpus_symbol, file_dir):
    def process_all_line():
        session = Session()
        corpus = session.query(db.Corpus).filter(
            db.Corpus.symbol == corpus_symbol).one()
        snkfiles = corpus.snkfiles
        session.close()

        for snkfile in snkfiles:
            for line in snkfile.readline(RAKUTEN_TRAVEL_DIR):
                extracted = corpus.extract_data(line)
                result =  {
                    'snkfile_id':snkfile.id,
                    'corpus_symbol': corpus.symbol,

                    'snkfile_id': snkfile.id,
                    'id_in_corpus': extracted['id_in_corpus'],
                    'contents': extracted['contents'],
                    'symbol': ''.join([
                        corpus.symbol,
                        '{:0>8}'.format(extracted['id_in_corpus'])
                    ])
                }
                LOGGER.info('proccess_file: ' + str(result['symbol']) + '  ' + result['contents'][:20])
                yield result

    def insert_original_datum(datum):
        insert_stmt = insert(db.OriginalData)
        on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(
            snkfile_id=insert_stmt.inserted.snkfile_id,
            id_in_corpus=insert_stmt.inserted.id_in_corpus,
            contents=insert_stmt.inserted.contents,
            symbol=insert_stmt.inserted.symbol,
        )
        with ENGINE.begin() as conn:
            conn.execute(on_duplicate_key_stmt, datum)

    datum = []
    max_size = 500_000_000
    for d in process_all_line():
        if sys.getsizeof(datum) < max_size:
            datum.append(d)
        else:
            LOGGER.info(f'INSERT: {len(datum)}件挿入!!!')
            insert_original_datum(datum)
            datum = []
    if datum:
        LOGGER.info(f'INSERT: {len(datum)}件挿入!!!')
        insert_original_datum(datum)

def insert_splitter(sname):
    s = db.Splitter(name=sname)

    _insert_single_record(s)

def insert_sentence(corpus_symbol, splitter_name):
    def iterate_all_sentence(splitter, snkfiles, mecab):
        for snkfile in snkfiles:
            session = Session()
            datum = snkfile.original_datum
            session.close()

            for data in datum:
                sentences = list(splitter.split(data.contents, mecab))
                n = len(sentences)

                for i, sentence in enumerate(sentences):
                    yield {
                        'data_id': data.id,
                        'symbol': f'{data.symbol}_{n:0>2}{i+1:0>2}',
                        'splitter_id': splitter.id,
                        'contents': sentence,
                        'sentence_number': i+1,
                        'sentence_number_max':n,
                    }

    def insert_sentences(sentence):
        insert_stmt = insert(db.Sentence)
        on_duplicate_key_stmt = insert_stmt.on_duplicate_key_update(
            contents=insert_stmt.inserted.contents,
            data_id=insert_stmt.inserted.data_id,
            symbol=insert_stmt.inserted.symbol,
            splitter_id=insert_stmt.inserted.splitter_id,
        )
        with ENGINE.begin() as conn:
            conn.execute(on_duplicate_key_stmt, sentence)
        LOGGER.info(f'INSERT: {len(sentences)}件挿入!!!')

    session = Session()

    sp = session.query(db.Splitter).filter(
        db.Splitter.name == splitter_name).one()

    snkfiles = session.query(db.SNKFile).filter(
        db.SNKFile.corpus.has(symbol=corpus_symbol))

    session.close()

    with MeCab() as mecab:
        itr = iterate_all_sentence(sp, snkfiles, mecab)

        sentences = []
        max_size = 500_000_000
        for s in itr:
            if sys.getsizeof(sentences) < max_size:
                LOGGER.info(f'{s["symbol"]}:\t\t{s["contents"]}')
                sentences.append(s)
            else:
                insert_sentences(sentences)
                sentences = []
        if sentence:
            insert_sentences(sentences)
